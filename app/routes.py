from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import News, Resources

@app.before_first_request
def init_db():
    db.create_all()

def get_news():
    return News.query.all()

def get_resources():
    return Resources.query.all()

@app.route('/')
def home():
    news = get_news()
    resources = get_resources()
    return render_template('index.html', news=news, resources=resources)

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search')
    news = News.query.filter(News.title.ilike(f'%{search_term}%')).all()
    resources = Resources.query.filter(Resources.title.ilike(f'%{search_term}%')).all()
    return render_template('index.html', news=news, resources=resources, search_term=search_term)

@app.route('/add_resource', methods=['POST'])
def add_resource():
    resource_title = request.form.get('resource_title')
    resource_type = request.form.get('resource_type')

    if resource_title and resource_type:
        new_resource = Resources(title=resource_title, type=resource_type)
        db.session.add(new_resource)
        db.session.commit()
        flash('Resource added successfully!', 'success')
    else:
        flash('Title and Type are required fields!', 'error')
    
    return redirect(url_for('home'))

@app.route('/update_resource/<int:id>', methods=['GET', 'POST'])
def update_resource(id):
    resource = Resources.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('update_resource.html', resource=resource)
    
    resource_title = request.form.get('resource_title')
    resource_type = request.form.get('resource_type')

    if resource_title and resource_type:
        resource.title = resource_title
        resource.type = resource_type
        db.session.commit()
        flash('Resource updated successfully!', 'success')
        return redirect(url_for('home'))
    
    flash('Title and Type are required fields!', 'error')
    return redirect(url_for('update_resource', id=id))

@app.route('/delete_resource/<int:id>', methods=['GET'])
def delete_resource(id):
    resource = Resources.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/post_info', methods=['POST'])
def post_info():
    print("Post new information action triggered!")
    return redirect(url_for('home'))