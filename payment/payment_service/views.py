from flask import Blueprint
# from .models import Author

test = Blueprint('test', __name__)

@test.route('/test')
def test_route():
    
    # author = Author(name=request.args.get('name', ''))
    # author.save()
    return 'HIII'

# @author_bp.route('/authors/')
# def list_authors():
#    """List all authors.     
#    e.g.: GET /authors"""
#    authors = Author.query.all()
#    content = '<p>Authors:</p>'
#    for author in authors:
#        content += '<p>%s</p>' % author.name
#    return content