<template>
  <div class="login">
    <div class="background">
      <el-image class="bgImg" :src="bgImg"></el-image>
    </div>
    <div class="front">
      <el-card>
        <span class="title">基于嵌入式软件的EFSM建模与安全测试用例集生成</span>
        <el-form class="loginForm" :model="loginForm" :rules="rules">
          <el-form-item prop="name">
            <el-input v-model="loginForm.name" placeholder="用户账号" value="test" style="width: 350px"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="密码" style="width: 350px"></el-input>
          </el-form-item>
        </el-form>
        <el-checkbox v-model="checked">记住密码</el-checkbox>
        <div class="action">
          <el-button type="primary" @click="gotolink" style="width: 180px">登录</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bgImg: require('@/assets/images/background.jpg'),
      loginForm: {
        name: '',
        password: '',
      },
      rules: {
        name: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 0, max: 10000, message: '长度在 3 到 5 个字符', trigger: 'blur' },
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
      checked: true,
    }
  },
  methods: {
    gotolink() {
      this.$http
        .post(this.Global_Api + '/api/login', { account: this.loginForm.name, password: this.loginForm.password })
        .then((response) => {
          if (response.data.error_code === 0) {
            // console.log(response.data.user)
            localStorage.setItem('user', response.data.user)
            this.remember()
            this.$store.commit('setUser', response.data.user_info)
            if (response.data.user_info.authority >= 2) this.$router.replace('/main')
            else {
              this.$store.commit('changeItem', 1)
              this.$router.replace('/itemMain')
            }
          } else {
            console.log(response.data)
            this.$message.error('用户名或密码错误！')
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    remember() {
      // console.log(data)
      if (this.checked) {
        // this.loginForm.name = 'admin'
        // this.loginForm.password = 'admin'
        this.setCookie(this.loginForm.name, this.loginForm.password, 7)
      } else {
        this.setCookie('', '', -1)
        // this.loginForm.name = ''
        // this.loginForm.password = ''
      }
    },
    // 设置cookie
    setCookie(name, pwd, exdays) {
      let exdate = new Date() // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays) // 保存的天数
      // 字符串拼接cookie
      window.document.cookie = 'userName' + '=' + name + ';path=/;expires=' + exdate.toGMTString()
      window.document.cookie = 'userPwd' + '=' + pwd + ';path=/;expires=' + exdate.toGMTString()
      // console.log('设置cookie', window.document.cookie)
    },
    // 读取cookie 将用户名和密码回显到input框中
    getCookie() {
      // console.log(window.document.cookie)
      if (window.document.cookie.length > 0) {
        let arr = document.cookie.split('; ') // 这里显示的格式需要切割一下自己可输出看下
        for (let i = 0; i < arr.length; i++) {
          let arr2 = arr[i].split('=') // 再次切割
          // 判断查找相对应的值
          if (arr2[0] === 'userName') {
            this.loginForm.name = arr2[1] // 保存到保存数据的地方
          } else if (arr2[0] === 'userPwd') {
            this.loginForm.password = arr2[1]
          }
        }
      }
    },
  },
  created() {
    this.getCookie()
  },
}
</script>

<style lang="scss">
.login {
  height: 100%;
  width: 100%;
}
.background {
  height: 100%;
  width: 100%;
  z-index: 0;
  position: absolute;
}
.bgImg {
  height: 100%;
}
.front {
  z-index: 1;
  position: absolute;
  margin-top: 15%;
  margin-left: 40%;
  width: 410px;
  height: 500px;
}
.loginForm {
  margin-top: 20px;
}
.action {
  margin-top: 20px;
  text-align: center;
}
</style>
