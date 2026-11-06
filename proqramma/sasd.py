from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import json
import os

window = Tk()
window.geometry('1920x1080')
window.resizable(False, False)
window.iconbitmap("favicon.ico")
window.title('Mystat')

image = Image.open('img.png')
image = image.resize((960, 1080))
photo = ImageTk.PhotoImage(image)

foto = Label(window, image=photo)
foto.place(x=960, y=0)


# Функции плейсхолдеров для авторизации
def on_focus_in(_):
    if log_entry.get() == placeholder_text:
        log_entry.delete(0, END)
        log_entry.config(fg='black')


def on_focus_out(_):
    if log_entry.get() == "":
        log_entry.insert(0, placeholder_text)
        log_entry.config(fg='grey')


def on_focus_in2(_):
    if password_entry.get() == placeholder_text2:
        password_entry.delete(0, END)
        password_entry.config(fg='black', show='*')


def on_focus_out2(_):
    if password_entry.get() == "":
        password_entry.config(show='')
        password_entry.insert(0, placeholder_text2)
        password_entry.config(fg='grey')


def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []


# Возврат на экран авторизации (Кнопка «Выйти»)
def logout(current_win):
    current_win.destroy()
    global window
    window = Tk()
    window.geometry('1920x1080')
    window.resizable(False, False)
    window.iconbitmap("favicon.ico")
    window.title('Mystat')

    # Повторная отрисовка главного экрана входа
    global foto, log_entry, password_entry
    image = Image.open('img.png')
    image = image.resize((960, 1080))
    photo = ImageTk.PhotoImage(image)
    foto = Label(window, image=photo)
    foto.place(x=960, y=0)

    mystat = Label(window, text='MyStat', fg='purple', font=('Arial', 30, 'bold'))
    mystat.place(x=5, y=5)

    login_label = Label(window, text='Login', fg='black', font=('Arial', 20, 'bold'))
    login_label.place(x=440, y=390)

    log_entry = Entry(window, fg='gray', width=20, font=('Arial', 25, 'bold'))
    log_entry.insert(0, placeholder_text)
    log_entry.place(x=300, y=450)
    log_entry.bind("<FocusIn>", on_focus_in)
    log_entry.bind("<FocusOut>", on_focus_out)

    password_entry = Entry(window, fg='gray', width=20, font=('Arial', 25, 'bold'))
    password_entry.place(x=300, y=550)
    password_entry.insert(0, placeholder_text2)
    password_entry.bind("<FocusIn>", on_focus_in2)
    password_entry.bind("<FocusOut>", on_focus_out2)

    log_btn = Button(window, text='Login', bg='purple', fg='white', width=18, font=('Arial', 25, 'bold'),
                     command=check_login)
    log_btn.place(x=300, y=650)
    window.mainloop()


# Показать подробную информацию о студенте (оценки и средний балл) при клике на имя
def show_student_details(student):
    details_win = Toplevel()
    details_win.geometry("400x300")
    details_win.title(f"Студент: {student.get('name')}")

    Label(details_win, text=f"Имя: {student.get('name')}", font=("Arial", 16, "bold")).pack(pady=10)
    Label(details_win, text=f"Логин: {student.get('login')}", font=("Arial", 14)).pack(pady=5)

    grades = student.get("grades", [])
    if grades:
        avg = round(sum(grades) / len(grades), 1)
        grades_str = ", ".join(map(str, grades))
    else:
        avg = "Нет оценок"
        grades_str = "Отсутствуют"

    Label(details_win, text=f"Оценки: {grades_str}", font=("Arial", 14)).pack(pady=5)
    Label(details_win, text=f"Средний балл: {avg}", font=("Arial", 14, "bold"), fg="purple").pack(pady=10)

    Button(details_win, text="Закрыть", command=details_win.destroy, font=("Arial", 12)).pack(pady=20)


# Функция удаления студента
def delete_student(login, teacher_win):
    if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить студента с логином '{login}'?"):
        users_list = load_users()
        users_list = [u for u in users_list if u.get("login") != login]

        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users_list, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Успех", "Студент удален.")
        teacher_win.destroy()
        open_teacher_window()


# Функция добавления нового студента
def add_new_student(name_entry, login_entry, pass_entry, teacher_win):
    name = name_entry.get().strip()
    login = login_entry.get().strip()
    password = pass_entry.get().strip()

    if not name or not login or not password:
        messagebox.showerror("Ошибка", "Все поля для нового студента должны быть заполнены!")
        return

    if login.lower() == "sama":
        messagebox.showerror("Ошибка", "Использовать логин 'sama' запрещено!")
        return

    users_list = load_users()
    for user in users_list:
        if user.get("login") == login:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
            return

    new_student = {
        "name": name,
        "login": login,
        "password": password,
        "role": "student",
        "grades": []
    }

    users_list.append(new_student)
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users_list, file, ensure_ascii=False, indent=4)

    messagebox.showinfo("Успех", f"Студент {name} успешно добавлен!")
    teacher_win.destroy()
    open_teacher_window()


# Сохранение оценок
def save_grades(entries_dict, teacher_win):
    users_list = load_users()

    for user in users_list:
        if user.get("role") == "student":
            login = user["login"]
            if login in entries_dict:
                val = entries_dict[login].get().strip()
                if val:
                    try:
                        grade = int(val)
                        if 1 <= grade <= 12:
                            if "grades" not in user:
                                user["grades"] = []
                            user["grades"].append(grade)
                        else:
                            messagebox.showerror("Ошибка", "Оценка должна быть от 1 до 12!")
                            return
                    except ValueError:
                        messagebox.showerror("Ошибка", "Введите целое число!")
                        return

    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users_list, file, ensure_ascii=False, indent=4)

    messagebox.showinfo("Успех", "Оценки успешно сохранены!")
    teacher_win.destroy()
    open_teacher_window()


# Окно преподавателя
def open_teacher_window():
    try:
        window.destroy()
    except TclError:
        pass
    teacher_win = Tk()
    teacher_win.geometry("1920x1080")
    teacher_win.title("Кабинет Преподавателя")

    Label(teacher_win, text="Управление студентами и оценками", font=("Arial", 22, "bold")).place(x=300, y=20)

    logout_btn = Button(teacher_win, text="Выйти", bg="red", fg="white", font=("Arial", 12, "bold"),
                        command=lambda: logout(teacher_win))
    logout_btn.place(x=980, y=20)

    users_list = load_users()
    entries_dict = {}

    y_pos = 90

    for user in users_list:
        if user.get("role") == "student":
            name = user.get("name", "")
            login = user.get("login", "")
            grades = user.get("grades", [])

            if len(grades) > 0:
                avg_grade = round(sum(grades) / len(grades), 1)
                avg_text = str(avg_grade)
            else:
                avg_text = "Нет оценок"

            name_btn = Button(teacher_win, text=f"{name} ({login})", font=("Arial", 14),
                              command=lambda u=user: show_student_details(u))
            name_btn.place(x=50, y=y_pos, width=250, height=35)

            Label(teacher_win, text=f"Ср. балл: {avg_text}", font=("Arial", 14), fg="gray").place(x=320, y=y_pos + 5)

            grade_entry = Entry(teacher_win, font=("Arial", 14), width=8)
            grade_entry.place(x=500, y=y_pos + 5)
            entries_dict[login] = grade_entry

            del_btn = Button(teacher_win, text="Удалить", bg="darkred", fg="white", font=("Arial", 10),
                             command=lambda l=login: delete_student(l, teacher_win))
            del_btn.place(x=620, y=y_pos + 5, width=80, height=30)

            y_pos += 50

    add_y = y_pos + 20
    Label(teacher_win, text="Добавить нового студента:", font=("Arial", 16, "bold")).place(x=50, y=add_y)

    Label(teacher_win, text="Имя:", font=("Arial", 12)).place(x=50, y=add_y + 40)
    new_name_entry = Entry(teacher_win, font=("Arial", 12), width=15)
    new_name_entry.place(x=90, y=add_y + 40)

    Label(teacher_win, text="Логин:", font=("Arial", 12)).place(x=250, y=add_y + 40)
    new_login_entry = Entry(teacher_win, font=("Arial", 12), width=15)
    new_login_entry.place(x=300, y=add_y + 40)

    Label(teacher_win, text="Пароль:", font=("Arial", 12)).place(x=460, y=add_y + 40)
    new_pass_entry = Entry(teacher_win, font=("Arial", 12), width=15, show="*")
    new_pass_entry.place(x=520, y=add_y + 40)

    add_btn = Button(teacher_win, text="Добавить студента", bg="green", fg="white", font=("Arial", 12, "bold"),
                     command=lambda: add_new_student(new_name_entry, new_login_entry, new_pass_entry, teacher_win))
    add_btn.place(x=680, y=add_y + 35)

    save_btn = Button(
        teacher_win,
        text="Сохранить оценки",
        bg="purple",
        fg="white",
        font=("Arial", 16, "bold"),
        command=lambda: save_grades(entries_dict, teacher_win)
    )
    save_btn.place(x=420, y=add_y + 100)

    teacher_win.mainloop()


# --- КАБИНЕТ СТУДЕНТА (ОБНОВЛЕННЫЙ) ---
def open_student_window(current_student):
    try:
        window.destroy()
    except TclError:
        pass

    student_win = Tk()
    student_win.geometry("1920x1080")
    student_win.title("Кабинет Студента")
    student_win.resizable(False, False)

    # Имя текущего студента
    name = current_student.get("name", "Студент")
    Label(student_win, text=f"Добро пожаловать, {name}!", font=("Arial", 22, "bold")).pack(pady=30)

    # Оценки студента
    grades = current_student.get("grades", [])

    # Безопасный расчет среднего балла (проверка на деление на ноль)
    if len(grades) > 0:
        avg_grade = round(sum(grades) / len(grades), 1)
        grades_text = ", ".join(map(str, grades))
    else:
        grades_text = "Оценок пока нет"
        avg_grade = "Нет оценок"

    Label(student_win, text=f"Ваши оценки: {grades_text}", font=("Arial", 16)).pack(pady=20)
    Label(student_win, text=f"Средний балл: {avg_grade}", font=("Arial", 18, "bold"), fg="purple").pack(pady=20)

    # Кнопка «Выйти»
    Button(
        student_win,
        text="Выйти",
        bg="red",
        fg="white",
        font=("Arial", 14, "bold"),
        command=lambda: logout(student_win)
    ).pack(pady=40)

    student_win.mainloop()


def check_login():
    user_login = log_entry.get()
    user_password = password_entry.get()

    users_list = load_users()
    found_user = None
    for user in users_list:
        if user.get("login") == user_login and user.get("password") == user_password:
            found_user = user
            break

    if found_user:
        messagebox.showinfo("Успех", "Вход выполнен!")
        if found_user.get("role") == "teacher":
            open_teacher_window()
        else:
            open_student_window(found_user)  # Передаем данные конкретного студента сюда
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")


# Первоначальный запуск окна авторизации
mystat = Label(window, text='MyStat', fg='purple', font=('Arial', 30, 'bold'))
mystat.place(x=5, y=5)

login_label = Label(window, text='Login', fg='black', font=('Arial', 20, 'bold'))
login_label.place(x=440, y=390)

log_entry = Entry(window, fg='gray', width=20, font=('Arial', 25, 'bold'))
placeholder_text = "E-mail or Login*"
log_entry.insert(0, placeholder_text)
log_entry.place(x=300, y=450)
log_entry.bind("<FocusIn>", on_focus_in)
log_entry.bind("<FocusOut>", on_focus_out)

password_entry = Entry(window, fg='gray', width=20, font=('Arial', 25, 'bold'))
password_entry.place(x=300, y=550)
placeholder_text2 = 'Password*'
password_entry.insert(0, placeholder_text2)
password_entry.bind("<FocusIn>", on_focus_in2)
password_entry.bind("<FocusOut>", on_focus_out2)

log_btn = Button(window, text='Login', bg='purple', fg='white', width=18, font=('Arial', 25, 'bold'),
                 command=check_login)
log_btn.place(x=300, y=650)

window.mainloop()