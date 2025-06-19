from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Quote, db

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
async def main_page():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        paginated_quotes = Quote.query.filter(Quote.user_id != current_user.id).paginate(page=page, per_page=2)
        return render_template('main.html', quotes=paginated_quotes)
    
    return render_template('main.html')

@main_blueprint.route('/add')
@login_required
async def add_quote():
    return render_template('add-quote.html')

@main_blueprint.route('/add', methods=['POST'])
@login_required
async def add_quote_post():
    text = request.form['text']
    
    quote = Quote(text=text, author=current_user)
    try:
        db.session.add(quote)
        db.session.commit()
        flash('Successfully added new quote', category='success')
        return redirect(url_for('main.main_page'))
    except Exception as e:
        print(e)
        flash('Something went wrong with database, please try again...', category='error')
        return redirect(url_for('main.add_quote'))

@main_blueprint.route('/profile')
@login_required
async def profile():
    page = request.args.get('page', 1, type=int)
    paginated_quotes = Quote.query.filter_by(author=current_user).paginate(page=page, per_page=2)
    return render_template('profile.html', quotes=paginated_quotes)

@main_blueprint.route('/profile', methods=['POST'])
async def avatar_change():
    filename = request.form['file']
    current_user.avatar = filename
    try:
        db.session.commit()
        return render_template('profile.html')
    except Exception as e:
        print(e)
        flash('Something went wrong with changing avatar, please try again...', category='error')
        return redirect(url_for('main.add_quote'))
    
@main_blueprint.route('/quote/<int:id>/update')
async def update_quote(id):
    quote = Quote.query.get_or_404(id)
    return render_template('update_quote.html', quote=quote)

@main_blueprint.route('/quote/<int:id>/update', methods=['POST'])
async def update_quote_post(id):
    quote = Quote.query.get_or_404(id)
    if not quote:
        flash('This quote is not exists', category='error')
        return redirect(url_for('main.main_page'))
    
    text = request.form['text']
    quote.text = text
    try:
        db.session.commit()
        flash('Successfully edited quote!', category='success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        print(e)
        flash('Something went wrong with database, please try again...', category='error')
        return redirect(url_for('main.main_page'))
    
@main_blueprint.route('/quote/<int:id>/delete')
async def delete_quote(id):
    quote = Quote.query.get_or_404(id)
    if not quote:
        flash('This quote is not exists', category='error')
        return redirect(url_for('main.main_page'))
    
    try:
        db.session.delete(quote)
        db.session.commit()
        flash('Successfully deleted quote!', category='success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        print(e)
        flash('Something went wrong with database, please try again...', category='error')
        return redirect(url_for('main.main_page'))