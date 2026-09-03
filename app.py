from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
load_dotenv()# تساعد على قراءة المتغيرات داخل .env

# render_template قالب العرض
# request جلب البيانات
# redirect اعادة التوجيه
# session أدارة الجلسات
# flash رسائل تظهر بعد ارسال البيانات
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY")  # التوقيع الخاص بالجلسة
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set")


@app.route("/")
def main():
    if "user_id" not in session:
        return redirect(url_for("login"))
    filter_task = request.args.get("filter", "all")  # إضافة قيمة افتراضية للفلتر
    user_id = session["user_id"]
    tasks = get_tasks(user_id, filter_task)
    return render_template("main.html", tasks=tasks, filter_task=filter_task)


@app.route("/add-task", methods=["post"])
def add_tasks():
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get(
        "title", ""
    ).strip()  # اذا لم يجد فلاسك شيء داخل الحقل النصي اعطني "" بدلاً من none
    if not title:
        return redirect(url_for("main"))
    user_id = session["user_id"]
    add_task(title, user_id)
    flash("تم إضافة المهمة بنجاح", "add_message")
    return redirect(url_for("main"))


@app.route("/login", methods=["post", "get"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()

        if not username or not password:
            flash("ادخل بيانات صحيحة", "error_message")
            return redirect(url_for("login"))

        
        user = get_user(username)
        if user is not None and check_password_hash(user["password"], password):
            session["username"] = username
            session["user_id"] = user["id"]
            return redirect(url_for("main"))
        flash("اسم المستخدم أو كلمة المرور خطأ", "error_message")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/register", methods=["post", "get"])
def register():
    if request.method == "POST":

        username = request.form.get("username","").strip() 
        password = request.form.get("password","").strip()

        if not username:
            flash("ادخل اسم مستخدم صالح", "invalid_message")
            return redirect(url_for("register"))
        
        if not password:
            flash("ادخل كلمة مرور صالحة", "invalid_message")
            return redirect(url_for("register"))
        
        user = get_user(username)
        if user is not None:
            flash("عذراً اسم المستخدم هذا موجود", "invalid_message")
            return redirect(url_for("register"))
        
        hashed_password = generate_password_hash(password)
        add_user(username, hashed_password)
        flash("تم تسجيل حساب جديد بنجاح ", "success_message")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/update-task", methods=["POST"])
def update_task():
    if "user_id" not in session:
        return redirect(url_for("login"))
    task_id = request.form.get("task_id")
    user_id = session["user_id"]
    completed = request.form.getlist("completed")[-1]
    update_task_status(task_id, completed, user_id)
    flash("تم تعديل المهمة بنجاح", "update_message")

    title = request.form.get("title")
    if title is not None:
        title = title.strip()
        if title:
            edit_task_from_db(title, task_id, user_id)

    return redirect(url_for("main"))


@app.route("/delete-task", methods=["POST"])
def delete_task():
    if "user_id" not in session:
        return redirect(url_for("main"))
    task_id = request.form.get("task_id")
    delete_task_from_db(task_id, session["user_id"])
    flash("تم حذف المهمة بنجاح", "delete_message")
    return redirect(url_for("main"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main"))
    total_tasks = get_total_tasks(session["user_id"])
    completed_tasks = get_completed_tasks_count(session["user_id"])
    uncompleted_tasks = get_uncompleted_tasks_count(session["user_id"])
    return render_template(
        "dashboard.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        uncompleted_tasks=uncompleted_tasks,
    )


@app.route("/update-username", methods=["POST"])
def update_username():
    if "user_id" not in session:
        return redirect(url_for("main"))
    new_username = request.form.get("new-username", "").strip()
    if not new_username:
        flash("ادخل اسم مستخدم صالح", "invalid")
        return redirect(url_for("dashboard"))
    user_id = session["user_id"]
    user = get_user(new_username)
    if user is not None:
        flash("عذراً اسم المستخدم هذا موجود", "invalid")
        return redirect(url_for("dashboard"))
    update_user(new_username, user_id)
    session["username"] = new_username
    flash("تم تحديث اسم المستخدم بنجاح", "successful")
    return redirect(url_for("dashboard"))


@app.route("/update-password", methods=["POST"])
def update_password():
    if "user_id" not in session:
        return redirect(url_for("main"))
    user_id = session["user_id"]
    old_password = request.form.get("old-password","").strip()
    new_password = request.form.get("new-password","").strip()
    user = get_user(session["username"])
    

    if user is None:
        session.clear()
        return redirect(url_for("login"))
    
    if not old_password or not check_password_hash(user["password"], old_password):
        flash("كلمة السر التي ادخلتها غير صحيحة", "invalid")
        return redirect(url_for("dashboard"))
    
    if not new_password:
        flash(" ادخل كلمة سر صحيحة", "invalid")
        return redirect(url_for("dashboard"))
    
    hashed_password = generate_password_hash(new_password)
    update_password_db(hashed_password, user_id)
    flash("تم تغيير كلمة السر بنجاح", "successful")
    return redirect(url_for("dashboard"))


@app.route("/delete", methods=["POST"])
def delete_user():
    if "user_id" not in session:
        return redirect(url_for("main"))
    delete_user_from_database(session["user_id"])
    session.clear()
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True, port=5000) #عند النشر يجب إيقاف debug
