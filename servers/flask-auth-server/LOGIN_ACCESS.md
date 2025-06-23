# Accessing Flask Authentication Server Login Page

To access the login page for the Flask authentication server, you can use the following URL:

**http://localhost:5001/**

Alternatively, you can also directly access:

**http://localhost:5001/auth/login**

## Plan to Access Flask Login Page

1.  **Identify Flask Server Port:**
    *   From `docker-compose.yml`, the `flask_auth_server` service maps container port `5000` to host port `5001` (`"5001:5000"`). This means the Flask server is accessible on your local machine at port `5001`.

2.  **Determine Flask Application Routes:**
    *   In `servers/flask-auth-server/app.py`, the Flask application is created and the `auth_bp` blueprint is registered with a URL prefix of `/auth` (`app.register_blueprint(auth_bp, url_prefix='/auth')`).
    *   The root route (`@app.route('/')`) in `app.py` redirects to `url_for('auth.login')`. This means if you access the base URL, it will automatically take you to the login page.

3.  **Locate Login Route within Blueprint:**
    *   In `servers/flask-auth-server/auth.py`, the login route is defined within the `auth_bp` blueprint as `@auth_bp.route('/login')`.

## Conclusion

Combining these points, the Flask authentication server is running on `localhost:5001`. The `/auth` prefix from the blueprint combined with the `/login` route within the blueprint means the login page is at `http://localhost:5001/auth/login`. Since the root URL `http://localhost:5001/` redirects to this login page, either URL will lead you to the login page.

```mermaid
graph TD
    A[User Accesses http://localhost:5001/] --> B{Flask App Root Route /};
    B --> C[Redirect to auth.login];
    C --> D[Access http://localhost:5001/auth/login];
    D --> E[Display Login Page];