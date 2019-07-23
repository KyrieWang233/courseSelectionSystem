from django.db import models


class User(models.Model):
    attribute = (
        ('teacher', '教师'),
        ('student', '学生'),
        ('admin', '管理员'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)  # 用户名（学号/工号）
    password = models.CharField(max_length=20)           # 用户密码
    kind = models.CharField(max_length=10, choices=attribute, default='学生')  # 用户属性 教师/学生
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Teacher(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 教师类与用户类一对一
    teacherID = models.CharField(max_length=20)                                       # 教师工号
    teacherName = models.CharField(max_length=20, null=True)                          # 教师姓名
    # 教师已开设课程，一对多，根据课程id寻找


class Student(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 学生类与用户类一对一
    studentID = models.CharField(max_length=20)                             # 学生学号
    studentName = models.CharField(max_length=20)                           # 学生姓名
    studentAddress = models.CharField(max_length=128, null=True)            # 学生区块链地址
    studentCredit = models.IntegerField(null=True)                          # 学生已获学分


class Admin(models.Model):
    id = models.OneToOneField(User, models.CASCADE, primary_key=True)    # 管理员类与用户类一对一


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=20)                           # 课程名称
    courseCredit = models.PositiveIntegerField()                           # 课程学分
    courseTeacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)   # 授课教师 与教师类一对多
    courseStudent = models.ManyToManyField(Student)                        # 课程学生 与学生类多对多


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    scoreStudent = models.ForeignKey(Student, on_delete=models.CASCADE)    # 成绩与学生一对多
    score_date = models.IntegerField(null=True)                            # 成绩分数
    scoreCourse = models.CharField(max_length=20, null=True)               # 成绩课程名
    scoreCredit = models.PositiveIntegerField()


class course_student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
