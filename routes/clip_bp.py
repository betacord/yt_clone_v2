from datetime import datetime

from flask import render_template, request, redirect, Blueprint, abort

from models.clip import ClipModel


# /
def index():
    newest_clips = ClipModel.newest(3)
    highest_rated = ClipModel.highest_rated(3)

    return render_template(
        'index.html',
        newest_clips=newest_clips,
        highest_rated=highest_rated
    )


# /add
def add_clip():
    if request.method == 'POST':
        req = request.form

        new_clip = ClipModel(
            title=req['title'],
            description=req['description'],
            link_yt=req['link_yt'],
            link_img=req['link_img'],
            added=datetime.timestamp(datetime.now()),
            score=0
        )
        new_clip.save()

        return redirect(request.url)

    return render_template('add.html')


def watch_clip(clip_id):
    if clip_details := ClipModel.find_by_id(clip_id):
        comments = clip_details.comments.all()
        clip_details.added = str(datetime.fromtimestamp(clip_details.added))[:19]

        return render_template('watch.html', clip=clip_details, comments=comments)

    abort(404)


def like_clip(clip_id):
    if clip := ClipModel.find_by_id(clip_id):
        clip.score += 1
        clip.save()

        return redirect(request.referrer)

    abort(404)


def unlike_clip(clip_id):
    if clip := ClipModel.find_by_id(clip_id):
        clip.score -= 1
        clip.save()

        return redirect(request.referrer)

    abort(404)


clip_bp = Blueprint('clip_bp', __name__)
# localhost:5000/
clip_bp.route('/', methods=['GET'])(index)
clip_bp.route('/add', methods=['GET', 'POST'])(add_clip)  # localhost:5000/add
clip_bp.route('/clip/<clip_id>')(watch_clip)  # localhost:5000/clip/4
clip_bp.route('/like_clip/<clip_id>', methods=['GET'])(like_clip)
clip_bp.route('/unlike_clip/<clip_id>', methods=['GET'])(unlike_clip)
