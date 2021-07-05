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
      bodyImg: require('@/assets/images/homePage2.jpg'),
      bodyMsg:
        '\xa0\xa0\xa0\xa0基于嵌入式软件的 EFSM 建模与安全测试用例集生成：' +
        '基于模型的测试用例自动生成软件使用的状态包括系统管理状态、测试需求建模状态、测试用例生成策略制定状态、测试用例生成状态。',
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
    height: 485px;
    width: 100%;
  }
}
</style>
