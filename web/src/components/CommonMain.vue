<template>
  <div id="common-main" v-show="vShow">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'CommonMain.vue',
  data() {
    return {
      itemInfo: '',
      vShow: true,
    }
  },
  methods: {
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('main', this.itemInfo)
      if (!this.itemInfo['name']) {
        this.vShow = false
      }
    },
  },
  mounted() {
    this.getItemInfo()
  },
}
</script>

<style scoped lang="scss">
#common-main {
  background: whitesmoke;
  height: 100%;
  width: 100%;
}
</style>
