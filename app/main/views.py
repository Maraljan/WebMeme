from pathlib import Path
from io import BytesIO

from flask import render_template, redirect, url_for, send_file
from flask_login import login_required, current_user

from . import main
from .forms import TemplateForm, MemeForm
from .. import db
from ..common.alerts import Alert, alert
from ..common.storage import ImageStorage
from ..models.meme import MemeTemplate, Meme
from ..services.image_processing import text_generate

template_storage = ImageStorage(Path('MemeTemplates'))
meme_storage = ImageStorage(Path('Meme'))


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')


@main.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
    form = TemplateForm()
    all_templates = MemeTemplate.query.filter_by(owner_id=current_user.pk)
    if form.validate_on_submit():
        file = form.img.data
        path = template_storage.save(file)
        template = MemeTemplate(
            title=form.title.data,
            owner_id=current_user.pk,
            image_path=str(path),
        )
        db.session.add(template)
        db.session.commit()
        alert('Uploading is successful.', Alert.SUCCESS)
    return render_template('templates.html', form=form, all_templates=all_templates)


@main.route('/create_meme/<title>', methods=['GET', 'POST'])
@login_required
def create_meme(title: str):
    template: MemeTemplate = MemeTemplate.query.filter_by(title=title, owner_id=current_user.pk).first()
    form = MemeForm()
    if form.validate_on_submit():
        abs_path = template_storage.get(template.image_path)
        edited_img = text_generate(form.text_top.data, form.text_bottom.data, abs_path)
        if form.save_to_desktop.data:
            abs_path = template_storage.get(template.image_path)
            edited_img = text_generate(form.text_top.data, form.text_bottom.data, abs_path)
            buffer = BytesIO()
            edited_img.save(buffer, format='PNG')
            buffer.seek(0)
            return send_file(
                path_or_file=buffer,
                as_attachment=True,
                attachment_filename=meme_storage.generate_filename('png')
            )
        else:
            meme_path = meme_storage.save(edited_img)
            meme = Meme(
                owner_id=current_user.pk,
                template_id=template.pk,
                image_path=str(meme_path),
            )
            db.session.add(meme)
            db.session.commit()
            alert('Saving is successful.', Alert.SUCCESS)
            return redirect((url_for('main.get_memes')))
    return render_template('create_meme.html', form=form, template=template)


@main.route('/meme', methods=['GET', 'POST'])
@login_required
def get_memes():
    all_memes = Meme.query.filter_by(owner_id=current_user.pk)
    return render_template('memes.html', memes=all_memes)


@main.route('/meme_download/<int:meme_id>')
def meme_download(meme_id: int):
    meme = Meme.query.filter_by(pk=meme_id, owner_id=current_user.pk).first()
    abs_path = meme_storage.get(meme.image_path)
    return send_file(str(abs_path), as_attachment=True)
