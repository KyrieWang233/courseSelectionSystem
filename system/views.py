from django.shortcuts import render, redirect
from .models import Course, Teacher, Student, User, Score, course_student
from .forms import UserForm, RegisterForm
course_reg_id = 0
student_inform_reg = []
student_inform = []
course_student_inform = []
course_inform_check = []


def index(request):
    pass
    return render(request, 'login/index.html')


def index_t(request):
    pass
    return render(request, 'login/index_t.html')


def index_s(request):
    pass
    return render(request, 'login/index_s.html')


def index_a(request):
    pass
    return render(request, 'login/index_a.html')


def tea1(request):
    if request.method == "POST":
        courseName = request.POST.get("courseName")
        courseCredit = request.POST.get("courseCredit")
        courseTeacher = request.session['user_id']
        Course.objects.create(courseName=courseName, courseCredit=courseCredit, courseTeacher_id=courseTeacher)
    return render(request, 'login/tea1.html')


def tea2(request):
    global student_inform_reg, course_reg_id, student_inform, course_student_inform
    student_inform_reg = []
    course_reg_id = 0
    student_inform = []
    course_student_inform = []
    if request.method == "GET":
        teacher_id = request.session['user_id']
        course_inform = Course.objects.filter(courseTeacher_id=teacher_id)
        context = {
            "course_inform": course_inform,
        }
        return render(request, 'login/tea2.html', context=context)
    else:
        course_reg_id = request.POST.get("course_id")
        course_student_inform = course_student.objects.filter(course_id=course_reg_id)
        for cs in course_student_inform:
            a = cs.student_id
            student_inform.append(a)
        for s in student_inform:
            a = Student.objects.filter(id_id=s).first()
            student_inform_reg.append(a)
        context = {
            "student_inform_reg": student_inform_reg
        }
        return render(request, 'login/reg_score.html', context=context)


def reg(request):
    global student_inform_reg, course_reg_id
    if request.method == "GET":
        context = {
            "student_inform_reg": student_inform_reg
        }
        return render(request, 'login/reg_score.html', context=context)
    else:
        score = request.POST.get("score")
        student_id = request.POST.get("student_id")
        studentobj = Student.objects.get(studentID=student_id)
        idid = studentobj.id_id
        course_obj = Course.objects.get(id=course_reg_id)
        cname = course_obj.courseName
        ccredit = course_obj.courseCredit
        new_score = Score.objects.create(scoreCourse=cname, score_date=score,
                                         scoreStudent_id=idid,scoreCredit=ccredit)
        new_score.save()
        return render(request, 'login/reg_score.html')


def stu1(request):
    courseStudent = request.session['user_id']
    if request.method == "GET":
        course_inform = Course.objects.all()
        context = {
            "course_inform": course_inform,
        }
        return render(request, 'login/stu1.html', context=context)
    else:
        course_add_id = request.POST.get("course_add_id")
        new_course_student = course_student.objects.create(course_id=course_add_id, student_id=courseStudent)
        new_course_student.save()
        return render(request, 'login/stu1.html')


def stu2(request):
    global course_inform_check
    course_inform_check = []
    inform2 = []
    student = request.session['user_id']
    inform = course_student.objects.filter(student_id=student)
    for c in inform:
        cid = c.course_id
        inform2.append(cid)
    for c in inform2:
        obj = Course.objects.get(id=c)
        course_inform_check.append(obj)
    score_inform = Score.objects.filter(scoreStudent_id=student)
    context = {
        "course_inform_check": course_inform_check,
        "score_inform": score_inform
    }
    return render(request, 'login/stu2.html', context=context)


def stu3(request):
    global course_inform_check
    credit = 0
    student = request.session['user_id']
    # for c in course_inform_check:
    #    credit += c.courseCredit
    for c in course_inform_check:
        cname = c.courseName
        score_check = Score.objects.filter(scoreCourse=cname).first()
        try:
            score = score_check.score_date
            if score >= 60:
                credit += c.courseCredit
            else:
                continue
        except AttributeError:
            credit += 0
    Student.objects.filter(id_id=student).update(studentCredit=credit)
    student_inform = Student.objects.filter(id_id=student)
    context = {
        "student_inform": student_inform,
    }
    return render(request, 'login/stu3.html', context=context)


def adm1(request):
    if request.method == "GET":
        student_inform = Student.objects.all()
        context = {
            "student_inform": student_inform,
        }
        return render(request, 'login/adm1.html', context=context)
    else:
        address = request.POST.get("address")
        student_id = request.POST.get("student_id")
        print(address)
        Student.objects.filter(studentID=student_id).update(studentAddress=address)
        return render(request, 'login/adm1.html')


def adm2(request):
    student_inform = Student.objects.all()
    context = {
        "student_inform": student_inform,
    }
    return render(request, 'login/adm2.html', context=context)


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            real_name = register_form.cleaned_data['real_name']
            id = register_form.cleaned_data['id']
            kind = register_form.cleaned_data['kind']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.kind = kind
                new_user.save()
                if kind == 'teacher':
                    new_tea = Teacher.objects.create(id_id=new_user.id)
                    new_tea.teacherName = real_name
                    new_tea.teacherID = id
                    new_tea.save()
                else:
                    new_stu = Student.objects.create(id_id=new_user.id)
                    new_stu.id_id = new_user.id
                    new_stu.studentName = real_name
                    new_stu.studentID = id
                    new_stu.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    if user.kind == 'teacher':
                        return redirect('/index_t/')
                    if user.kind == 'admin':
                        return redirect('/index_a/')
                    else:
                        return redirect('/index_s/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
