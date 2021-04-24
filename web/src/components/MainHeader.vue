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
    <div id="bottom2">
      <el-menu
        router
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        :default-active="$route.path"
      >
        <el-submenu index="1">
          <template slot="title">平台信息管理</template>
          <el-submenu index="1-1">
            <template slot="title">系统管理</template>
            <el-menu-item index="/personnel">人员管理</el-menu-item>
            <el-menu-item index="/authority">权限管理</el-menu-item>
            <el-menu-item index="/tools">工具说明</el-menu-item>
          </el-submenu>
          <el-menu-item index="/item">项目管理</el-menu-item>
        </el-submenu>
        <!--        <el-submenu index="2">-->
        <!--          <template slot="title">安全性数据库管理</template>-->
        <!--          <el-menu-item index="/analysisBase">分析规则库</el-menu-item>-->
        <!--          <el-menu-item index="/designBase">设计准则库</el-menu-item>-->
        <!--          <el-menu-item index="/failureDataBase">失效数据库</el-menu-item>-->
        <!--        </el-submenu>-->
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonHeader.vue',
  data() {
    return {
      title: '基于嵌入式软件的 EFSM 建模与安全测试用例集生成',
      imgLogo: require('@/assets/images/logo.png'),
      activeIndex: '2',
      divSubMenuVisible: false,
      itemInfo: {
        item_content: '',
        item_date: null,
        item_id: 0,
        item_introduction: '',
        item_name: '',
      },
      headMenu: [],
    }
  },
  mounted() {
    this.getItemInfo()
    this.activeIndex = this.$route.path
    // console.log(this.itemInfo)
  },
  methods: {
    gotoHome() {
      this.$router.replace('/main')
    },
    gotoLogin() {
      // window.location.href = '/'
      this.$router.replace('/login')
    },
    getItemInfo() {
      this.bus.$on('itemInfo', (msg) => {
        this.itemInfo = msg
        console.log(this.itemInfo)
        this.divSubMenuVisible = true
      })

      // this.divSubMenuVisible = true
    },
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
    height: 60px;
    #left-content {
      width: 100%;
      display: flex;
      #imgLogo {
        //height: 60px;
        width: 65px;
      }
      #leftTitle {
        height: 60px;
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
    background: #b4d2ea;
    #tab {
      display: flex;
    }

    height: 100%;
    //width: 100%;
    background: #545c64;
    display: flex;
    #mainMenu {
      height: 100%;
      //width: 60%;
      #el-menu {
        display: flex;
        height: 100%;
        width: 100%;
      }
    }
    //#subMenu {
    //  width: 400px;
    //  height: 100%;
    //  //background: greenyellow;
    //  #itemTitle {
    //    height: 40%;
    //    margin-top: 5.5px;
    //    margin-left: 45%;
    //    //text-align: center;
    //    background: greenyellow;
    //  }
    //  #itemMenu {
    //    height: 50%;
    //    margin-top: 0;
    //    background: yellow;
    //  }
    //}
  }
}

#itemMenu {
  //background: white;
  //background: #545c64;
  display: flex;
  //height: 80%;
}
#headMenu {
  //background: gold;
  background: #545c64;
  display: flex;
}
</style>
<style lang="scss">
.itemMenu {
  .el-menu-item {
    height: 95%;
    //margin-top: 10px;
    background: #545c64;
    //display: flex;
  }
  .el-button {
    width: 20px;
    height: 20px;
    padding: 0;
    margin-top: 15px;
    margin-left: 15px;
    margin-right: 15px;
  }
}
.itemTitle {
  .el-button {
    //height: 10px;
    //border: 0;
    padding: 0;
    margin: 0 0 0 60%;
  }
}
.leftCube {
  width: 130px;
  height: 40px;
  border: whitesmoke 1px solid;
  background: #d7e7f2;
  color: #333;
  margin-left: 30px;
  border-top-left-radius: 5px;
  filter: progid:DXImageTransform.Microsoft.Shadow(color=#909090,direction=120,strength=4);
  -moz-box-shadow: 2px 2px 10px #909090; /*firefox*/
  -webkit-box-shadow: 2px 2px 10px #909090; /*safari或chrome*/
  box-shadow: 2px 2px 10px #909090; /*opera或ie9*/
}
.cube {
  width: 130px;
  height: 40px;
  border: whitesmoke 1px solid;
  background: #d7e7f2;
  margin-left: -1px;
  color: #333;
  filter: progid:DXImageTransform.Microsoft.Shadow(color=#909090,direction=120,strength=4);
  -moz-box-shadow: 2px 2px 10px #909090; /*firefox*/
  -webkit-box-shadow: 2px 2px 10px #909090; /*safari或chrome*/
  box-shadow: 2px 2px 10px #909090; /*opera或ie9*/
}
.rightCube {
  width: 130px;
  height: 40px;
  border: whitesmoke 1px solid;
  background: #d7e7f2;
  margin-left: -1px;
  color: #333;
  border-top-right-radius: 5px;
  filter: progid:DXImageTransform.Microsoft.Shadow(color=#909090,direction=120,strength=4);
  -moz-box-shadow: 2px 2px 10px #909090; /*firefox*/
  -webkit-box-shadow: 2px 2px 10px #909090; /*safari或chrome*/
  box-shadow: 2px 2px 10px #909090; /*opera或ie9*/
}
</style>
