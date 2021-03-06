Project: build an catalog application 

## File Structure
- `project.py`: contains all @app.route 
- `common.py`: contains related defs
- `signin.py`: contains authentication & authorization signin
- `database_setup.py`: It will set up database using sqlalchemy
- `researchoption.db`: This file is generated by running `database_setup.py`
- `templates`: html templates folder for flask
- `static`: static folder which includes js, css, img for flask
- `Gruntfile.js`: Grunt file to convert SCSS to CSS
- `Gruntfile.yml`: Same as the above
- `package-lock.json`: npm package for Grunt usage
- `package.json`: Same as the above
- `node_modules`: Same as the above


## DB structure
Database has the following tables:
- Category: contains 6 categoris, each of which has `name` and `description`.
- Option: each option has `nama`, `description`, `cat_id`(foreign key of Category.id) and `user_id`(User.id)
- Link: each link has `title`, `url`, and `option_id`(foreign key of Option.id)
- User: each user has `name` and `email`.

## Page structure
- `/`: shows 6 category
- `/<string:category_name>`: to show list of options with the selected category
- `/<string:category_name>/<int:option_id>`: to show contents of the selected option including related links
- `/<string:category_name>/new`: to add new option
- `/<string:category_name>/<int:option_id>/edit`: to edit or delete the selected option and related links

The following are execution only: 
- `/<string:category_name>/<int:option_id>/delete`: to delete the option
- `/<string:category_name>/<int:option_id>/newlink`: to add new link
- `/<string:category_name>/<int:option_id>/<int:link_id>/delete`: to delete the link 

The following are for JSON format:
- `/<string:category_name>/JSON`: returns all options in the category
- `/<string:category_name>/<int:option_id>/JSON`: returns all option contents

## License
[MIT License](https://choosealicense.com/licenses/mit/) © [Yukino Kohmoto](http://yukinokoh.github.io/)
 

