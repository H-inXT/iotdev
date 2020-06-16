from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from dev.models import Product

# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#   def render(self):
#     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名', 
        widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'}))
    #                                          定义文本框的样式 PassIn..这本身是一个类 然后attr传入字典
    password = forms.CharField(label='密码', 
                                widget=forms.PasswordInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    # user = forms.CharField(
    #         label='用户名',
    #         initial=2,
    #         widget=forms.Select(choices=((1,'上海'),(2,'北京'),)
    #         )
    # )

    # hobby = forms.fields.ChoiceField(
    #     choices=((1, "篮球"), (2, "足球"), (3, "双色球"), ),
    #     label="爱好",
    #     initial=3,
    #     widget=forms.RadioSelect(renderer=HorizontalRadioRenderer)
    # )
    # gender = forms.ChoiceField(
    #     choices=((1, '男'), (2, '女'),),
    #       # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
    #     initial=2,  # 默认选中第二个option
    #     widget=forms.RadioSelect()  # 插件表现形式为单选按钮
    # )
    # hobby=forms.fields.CharField(
    #     widget=forms.widgets.RadioSelect(choices=[(1,"男"),(2,"女"),]),   #单选radio
    #     initial = 2,
    # )

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
            
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', 
                                max_length=30,
                                min_length=3,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入3-30位的用户名'}))
    email = forms.EmailField(label='邮箱', 
                                widget=forms.EmailInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    
    verification_code = forms.CharField(label='验证码',    
                                required=False,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送验证码'}))
    
    password = forms.CharField(label='密码', 
                                min_length=6,
                                widget=forms.PasswordInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再次输入密码', 
                                    min_length=6,
                                    widget=forms.PasswordInput(
                                                    attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request') # 弹出并赋值
        super(RegForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释
    
    def clean(self):
        # 判断验证码
        # code = self.request.session.get('bind_email_code', '')
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data
    

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('输入的两次密码不一致')
        return password_again
    
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code
    

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='昵称',
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user') # 弹出并赋值
        super(ChangeNicknameForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError("新的昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击”发送验证码“发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request') # 弹出并赋值
        super(BindEmailForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登陆')

        # 判断用户是否登录
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入旧的密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )
    newpassword_again = forms.CharField(
        label='请再次输入新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user') # 弹出并赋值
        super(ChangePasswordForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean(self):
        # 验证新的密码是否一致 并且新旧密码不一样
        old_password = self.cleaned_data.get('old_password', '')
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('newpassword_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        if old_password == new_password:
            raise forms.ValidationError('新旧密码不可以一样')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password

class ForgotPasswordForm(forms.Form):
    # 也可以是通过用户名来修改密码， 33
    email = forms.EmailField(
        label='邮箱',
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击”发送验证码“发送到邮箱'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request') # 弹出并赋值
        super(ForgotPasswordForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean_username(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('用户名不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code


class RegProductForm(forms.Form):
    product_name = forms.CharField(label='产品名称', 
                                max_length=30,
                                min_length=3,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入3-30位的产品名'}))

    # gender = forms.fields.ChoiceField(
    #     choices=((1, "男"), (2, "女"), (3, "保密")),
    #     label="性别",
    #     initial=3,
    #     widget=forms.widgets.RadioSelect()
    # )

    industry = forms.CharField(label='产品行业', 
                                max_length=30,
                                min_length=3,   
                                required=False,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入产品行业（3-30字符）'}))

    internet_connect = forms.CharField(
            label='联网方式',
            initial='移动蜂窝网络',
            widget=forms.Select(choices=(('wifi', 'wifi'),('移动蜂窝网络', '移动蜂窝网络'),)
            )
    )

    protocol = forms.CharField(
            label='接入协议',
            initial='MQTT',
            widget=forms.Select(choices=(('MQTT', 'MQTT'),('UDP', 'UDP'),('HTTP','HTTP'),)
            )
    )

    system = forms.CharField(
            label='系统',
            initial=2,
            widget=forms.Select(choices=(('Linux', 'Linux'),('Android', 'Android'),('Vxworks', 'Vxworks'),('uC/Os', 'uC/Os'),('无', '无'),)
            )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user') # 弹出并赋值
        super(RegProductForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['pro_user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        return self.cleaned_data

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('用户名已存在')
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('邮箱已存在')
    #     return email

    # def clean_password_again(self):
    #     password = self.cleaned_data['password']
    #     password_again = self.cleaned_data['password_again']
    #     if password != password_again:
    #         raise forms.ValidationError('输入的两次密码不一致')
    #     return password_again

    # def clean_verification_code(self):
    #     verification_code = self.cleaned_data.get('verification_code', '').strip()
    #     if verification_code == '':
    #         raise forms.ValidationError('验证码不能为空')
    #     return verification_code

'''
class RegDeviceForm(forms.Form):

    device_name = forms.CharField(label='设备名称', 
                            max_length=30,
                            min_length=3,
                            widget=forms.TextInput(
                                            attrs={'class':'form-control', 'placeholder':'请输入3-30位的产品名'}))

    pro = Product.objects.all()
    # for i in pro:
    #     i.append(i)
    product = forms.CharField(
            label='所属产品',
            initial='',
            widget=forms.Select(choices=pro)
            )

    authentication = forms.CharField(label='鉴权信息', 
                                max_length=30,
                                min_length=3,   
                                required=False,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入产品行业（3-30字符）'}))

    describe = forms.CharField(label='描述', 
                                max_length=30,
                                min_length=3,   
                                required=False,
                                widget=forms.TextInput(
                                                attrs={'class':'form-control', 'placeholder':'请输入产品行业（3-30字符）'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user') # 弹出并赋值
        super(RegDeviceForm, self).__init__(*args, **kwargs) # 详情看32:20左右的解释

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['pro_user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        return self.cleaned_data
'''

