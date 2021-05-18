from pathlib import Path

from flask import render_template
from flask_login import login_required, current_user

from . import main
from .forms import TemplateForm
from .. import db
from ..common.alerts import Alert, alert
from ..common.storage import ImageStorage
from ..models.meme import MemeTemplate

storage = ImageStorage(Path('Test'))


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
        path = storage.save(file)
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
    template = MemeTemplate.query.filter_by(title=title, owner_id=current_user.pk).first()
    return render_template('create_meme.html', template=template)
