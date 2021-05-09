<template>
  <div id="common-header" class="common-header">
    <div id="top">
      <div id="left-content">
        <div id="imgLogo">
          <el-image :src="imgLogo"></el-image>
        </div>
        <div id="leftTitle">
          <span>{{ title }}</span>
        </div>
      </div>
      <div id="right-content">
        <div id="rightTitle">
          <el-link @click="gotoHome">首页</el-link> |
          <el-link @click="gotoLogin">退出</el-link>
        </div>
      </div>
    </div>
    <div id="bottom" v-if="user.authority > 1">
      <span style="font-weight: bold; margin-left: 50px">{{ itemInfo.name }}</span>
      <el-button type="text" style="margin-left: 20px" @click="gotoItemMember">管理项目成员</el-button>
      <!--      <el-button type="text" style="margin-left: 20px" @click="testSave">保存</el-button>-->
      <el-button type="text" style="margin-left: 20px" @click="gotoItem">关闭</el-button>
    </div>
    <div id="bottom2" v-else>
      <el-select v-model="value" placeholder="请选择" @change="onchange" style="float: right">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonHeader.vue',
  inject: ['reload'],
  data() {
    return {
      value: '',
      title: '基于嵌入式软件的 EFSM 建模与安全测试用例集生成',
      imgLogo: require('@/assets/images/logo.png'),
      activeIndex: '2',
      user: '',
      tableData: '',
      options: [],
      divSubMenuVisible: false,
      itemInfo: '',
      headMenu: [],
      userInfo: '',
    }
  },
  mounted() {
    this.getItemInfo()
    this.activeIndex = this.$route.path
    let value1 = this.$store.state.user
    this.user = value1
    this.getUserItem()
    // console.log('this.itemInfo', this.itemInfo)
    // if (this.itemInfo.name === ' ') {
    // }
  },
  methods: {
    onchange() {
      console.log('value', this.value)
      this.$http.post(this.Global_Api + '/api/get_item', { name: this.value }).then((response) => {
        let item = response.data.item
        this.$store.commit('changeItem', item)
        this.reload()
      })
    },
    // handleSelect(key, keyPath) {
    //   // console.log(key, keyPath)
    //   // console.log(this.menuList[key])
    //   this.bus.$emit('transferMenuData', this.menuList[key])
    // },
    // selectAnalysis() {
    //   this.bus.$emit('transferMenuData', this.menuList[0])
    // },
    // selectDesign() {
    //   this.bus.$emit('transferMenuData', this.menuList[1])
    // },
    // closeSubMenu() {
    //   this.divSubMenuVisible = false
    //   this.bus.$emit('transferMenuData', this.menuList[2])
    // },
    gotoHome() {
      this.$router.replace('/main')
    },
    gotoLogin() {
      this.$router.replace('/login')
    },
    gotoItemMember() {
      this.$router.replace('/itemMember')
    },
    gotoItem() {
      this.$router.replace('/item')
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      this.value = this.itemInfo.name
      // console.log('header', this.itemInfo)
      // console.log('header', this.value)
    },
    getUserInfo() {
      this.userInfo = this.$store.state.user
    },
    testSave() {
      this.$http.post(this.Global_Api + '/api/report', { item: this.itemInfo }, { responseType: 'blob' }).then((data) => {
        console.log(data)
        let objectUrl = URL.createObjectURL(data.data)
        const link = document.createElement('a') // 创建a标签
        link.download = '（公开）软件安全性工作报告模板.docx' // a标签添加属性
        link.style.display = 'none'
        link.href = objectUrl
        document.body.appendChild(link)
        link.click() // 执行下载
        URL.revokeObjectURL(link.href) // 释放url
        document.body.removeChild(link) // 释放标签
      })
    },
    getUserItem() {
      // console.log(this.userInfo)
      this.$http.post(this.Global_Api + '/api/user_item', this.userInfo).then((response) => {
        this.tableData = response.data.item_list
        // console.log(this.tableData)
        this.options = []
        for (let i = 0; i < this.tableData.length; i++) {
          this.options.push({ value: this.tableData[i].item_name, label: this.tableData[i].item_name })
        }
        this.value = this.itemInfo.name
      })
    },
  },
  // created: function() {
  //   console.log('a is:' + this.a)
  //   this.$http
  //     .get(this.Global_Api + '/api/item_list')
  //     .then(response => {
  //       this.tableData = response.data.item_list
  //       console.log(this.tableData)
  //       this.options = []
  //       for (let i = 0; i < this.tableData.length; i++) {
  //         this.options.push({ value: this.tableData[i].id, label: this.tableData[i].name })
  //       }
  //       this.value = this.itemInfo.name
  //     })
  //     .catch(function(error) {
  //       console.log(error)
  //     })
  // },
  created() {
    this.getUserInfo()
    this.getItemInfo()
  },
}
</script>

<style scoped lang="scss">
#common-header {
  background: #f5f9f9;
  width: 100%;
  height: 100px;
  display: flex;
  flex-direction: column;
  #top {
    display: flex;
    //height: 60px;
    #left-content {
      width: 100%;
      display: flex;
      #imgLogo {
        //height: 60px;
        width: 65px;
      }
      #leftTitle {
        //height: 60px;
        font-size: xx-large;
        font-weight: bold;
        font-family: 楷体;
        margin-top: 10px;
        margin-left: 20px;
      }
    }
    #right-content {
      width: 100px;
      float: right;
      #rightTitle {
        margin-top: 20px;
      }
    }
  }
  #bottom {
    height: 40px;
    background: #b4d2ea;
    margin-top: -2px;
  }
  #bottom2 {
    height: 40px;
    background: #b4d2ea;
    margin-top: -2px;
  }
}
</style>
