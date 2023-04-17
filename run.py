from Flask_BLOG import app, db

if __name__ == '__main__':
    # with app.app_context():
        
    #     # user_1 = User(username='saithim', email='s@mail.com',password='hey')
    #     # db.session.add(user_1)
    #     # User.query.all()
    #     # db.create_all()
    #     # db.session.commit()
    #     db.drop_all()
        
    with app.app_context():
        db.create_all()
    app.run(debug=True)