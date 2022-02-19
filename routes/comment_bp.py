from flask import Blueprint, request, redirect, abort

from models.comment import CommentModel

comment_bp = Blueprint('comment_bp', __name__)


def add_comment():
    if request.method == 'POST':
        req = request.form

        new_comment = CommentModel(
            author=req['author'],
            content=req['content'],
            clip_id=req['clip_id']
        )
        new_comment.save()

        return redirect(request.referrer)

    abort(405)


def remove_comment():
    if request.method == 'POST':
        req = request.form

        comment = CommentModel.find_by_id(req['id'])
        comment.remove()

        return redirect(request.referrer)

    abort(405)


comment_bp.route('/add', methods=['POST'])(add_comment)  # localhost:5000/comment/add
comment_bp.route('/remove', methods=['POST'])(remove_comment)  # localhost:5000/comment/remove
