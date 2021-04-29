<template>
  <div id="common-aside">
    <div id="aside-content" style="height: 100%">
      <el-menu router :default-active="$route.path" style="height: 100%" :unique-opened="true">
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>模型</span>
          </template>
          <el-menu-item index="/xmiImport"><i class="el-icon-folder"></i>XMI文件导入</el-menu-item>
          <el-submenu index="1-1">
            <template slot="title"><i class="el-icon-folder"></i>静态模型构建</template>
            <el-menu-item index="/"><i class="el-icon-folder"></i>模型描述</el-menu-item>
            <el-menu-item index="/"><i class="el-icon-folder"></i>模型查看与编辑</el-menu-item>
          </el-submenu>
          <el-submenu index="2-1">
            <template slot="title"><i class="el-icon-folder"></i>动态模型构建</template>
            <el-menu-item index="/modelInfo"><i class="el-icon-folder"></i>模型描述</el-menu-item>
            <el-menu-item index="/modelEdit"><i class="el-icon-folder"></i>模型查看与编辑</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>测试生成</span>
          </template>
          <el-submenu index="2-1">
            <template slot="title"><i class="el-icon-folder"></i>路径生成准则</template>
            <el-menu-item index="/fullState"><i class="el-icon-folder"></i>全状态</el-menu-item>
            <el-menu-item index="/fullMigration"><i class="el-icon-folder"></i>全迁移</el-menu-item>
          </el-submenu>
          <el-submenu index="2-2">
            <template slot="title"><i class="el-icon-folder"></i>数据生成准则</template>
            <el-menu-item index="/increase"><i class="el-icon-folder"></i>递增值</el-menu-item>
            <el-menu-item index="/decrease"><i class="el-icon-folder"></i>递减值</el-menu-item>
            <el-menu-item index="/boundaryValue"><i class="el-icon-folder"></i>边界值</el-menu-item>
            <el-menu-item index="/randomValue"><i class="el-icon-folder"></i>随机值</el-menu-item>
            <el-menu-item index="/mcDcCoverage"><i class="el-icon-folder"></i>MC/DC覆盖</el-menu-item>
            <!--            <el-menu-item index="/interfaceProtocol"><i class="el-icon-folder"></i>接口协议</el-menu-item>-->
          </el-submenu>
          <!--          <el-menu-item index="/communicationProtocol"><i class="el-icon-folder"></i>通信协议</el-menu-item>-->
        </el-submenu>
        <!--        <el-menu-item index="/script"><i class="el-icon-folder"></i>脚本</el-menu-item>-->
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonAside.vue',
  data() {
    return {
      asideMenu: [],
      value: '',
      options: [
        {
          value: 'ss',
          label: 'ss',
        },
      ],
      itemInfo: 'test',
    }
  },
  methods: {
    clickMenu(item) {
      if (this.$route.name !== item.name) {
        this.$router.push({ name: item.name })
      }
      // this.$store.commit('selectMenu', item)
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('item', this.itemInfo)
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath + '关闭')
    },
  },
  mounted() {
    this.getItemInfo()
  },
  updated() {
    this.getItemInfo()
  },
  created() {
    this.getItemInfo()
  },
  computed: {},
}
</script>

<style scoped lang="scss">
#common-aside {
  background: lightyellow;
  width: 100%;
  height: 653px;
  font-weight: bold;
  //display: flex;
  #aside-content {
    width: 100%;
    height: 100%;
  }
}
</style>
