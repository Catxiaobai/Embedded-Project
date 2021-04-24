<template>
  <div id="home">
    <div id="body">
      <el-card id="bodyCard">
        <el-image class="bodyImg" :src="bodyImg"> </el-image>
        <!--        <el-input class="bodyMsg" type="textarea" autosize v-model="bodyMsg"> </el-input>-->
        <p style="font-weight: bold; font-size: 30px; font-family: 楷体; line-height: 40px">
          {{ bodyMsg }}
        </p>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      bodyImg: require('@/assets/images/homePage.jpg'),
      bodyMsg:
        '\xa0\xa0\xa0\xa0基于嵌入式软件的 EFSM 建模与安全测试用例集生成。' +
        '文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述' +
        '文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述' +
        '文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述文本描述。',
    }
  },
  methods: {},
}
</script>

<style scoped lang="scss">
#body {
  height: 100%;
  width: 100%;
}
</style>
<style lang="scss">
.bodyMsg {
  .el-textarea__inner {
    border: none;
    resize: none;
    font-weight: bold;
    font-size: 24px;
    font-family: 楷体;
  }
}
.bodyImg {
  width: 100%;
  .el-image__inner {
    height: 435px;
    width: 100%;
  }
}
</style>
