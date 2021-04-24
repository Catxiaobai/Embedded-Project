<template>
  <div id="common-aside">
    <div id="aside-content" style="height: 100%">
      <el-menu router :default-active="$route.path" style="height: 100%" :unique-opened="true">
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>模型</span>
          </template>
          <el-menu-item index="/requirements"><i class="el-icon-folder"></i>XMI文件导入</el-menu-item>
          <el-submenu index="1-1">
            <template slot="title"><i class="el-icon-folder"></i>模型构建</template>
            <el-menu-item index="/subSceneInfo"><i class="el-icon-folder"></i>模型描述</el-menu-item>
            <el-menu-item index="/subSceneShow"><i class="el-icon-folder"></i>模型查看与编辑</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>测试生成</span>
          </template>
          <el-submenu index="2-1">
            <template slot="title"><i class="el-icon-folder"></i>路径生成准则</template>
            <el-menu-item index="/generalCriteria"><i class="el-icon-folder"></i>全状态</el-menu-item>
            <el-menu-item index="/specialCriteria"><i class="el-icon-folder"></i>全迁移</el-menu-item>
          </el-submenu>
          <el-submenu index="2-2">
            <template slot="title"><i class="el-icon-folder"></i>数据生成准则</template>
            <el-menu-item index="/generalCriteria"><i class="el-icon-folder"></i>边界值</el-menu-item>
            <el-menu-item index="/specialCriteria"><i class="el-icon-folder"></i>随机值</el-menu-item>
            <el-menu-item index="/specialCriteria"><i class="el-icon-folder"></i>接口协议</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-menu-item index="/specialCriteria"><i class="el-icon-folder"></i>脚本库</el-menu-item>
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
  height: 100%;
  font-weight: bold;
  //display: flex;
  #aside-content {
    width: 100%;
    height: 100%;
  }
}
</style>
