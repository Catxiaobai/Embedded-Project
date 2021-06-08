<template>
  <div>
    <el-card style="height: 653px">
      <!--      <div>-->
      <!--        <el-form :inline="true" :model="formInline" class="demo-form-inline">-->
      <!--          <el-form-item label="主题名称">-->
      <!--            <el-input v-model="formInline.name" placeholder="主题名称"></el-input>-->
      <!--          </el-form-item>-->
      <!--          <el-form-item label="日期">-->
      <!--            <el-input v-model="formInline.date" placeholder="日期"></el-input>-->
      <!--          </el-form-item>-->
      <!--          <el-form-item label="版本">-->
      <!--            <el-input v-model="formInline.version" placeholder="版本"></el-input>-->
      <!--          </el-form-item>-->
      <!--        </el-form>-->
      <!--        <el-form :inline="true" :model="formInline" class="demo-form-inline">-->
      <!--          <el-form-item label="总线类型">-->
      <!--            <el-input v-model="formInline.type" placeholder="总线类型"></el-input>-->
      <!--          </el-form-item>-->
      <!--          <el-form-item label="通讯方式">-->
      <!--            <el-input v-model="formInline.method" placeholder="通讯方式"></el-input>-->
      <!--          </el-form-item>-->
      <!--          <el-form-item label="刷新周期">-->
      <!--            <el-input v-model="formInline.period" placeholder="刷新周期"></el-input>-->
      <!--          </el-form-item>-->
      <!--        </el-form>-->
      <!--      </div>-->
      <div>
        <p style="margin-bottom: 20px">主题名称：{{ info.subjectName }}</p>
        <p style="margin-bottom: 20px">日期：{{ info.date }}</p>
        <p style="margin-bottom: 20px">版本：{{ info.version }}</p>
        <p style="margin-bottom: 20px">总线类型：{{ info.busType }}</p>
        <p style="margin-bottom: 20px">通讯方式：{{ info.communicationMethod }}</p>
        <p style="margin-bottom: 20px">刷新周期：{{ info.refreshCycle }}</p>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 400px">
          <el-table-column prop="id" label="序号"> </el-table-column>
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="describe" label="内容">
            <!--            <template slot-scope="scope">-->
            <!--              <el-select v-model="scope.row.describe" filterable allow-create default-first-option style="border: 0; margin: 0; padding: 0" @change="frame">-->
            <!--                <el-option v-for="item in scope.row.options" :key="item.value" :label="item.label" :value="item.value"> </el-option>-->
            <!--              </el-select>-->
            <!--            </template>-->
          </el-table-column>
        </el-table>
      </div>
      <!--      <el-button type="primary" style="margin-left: 40%; margin-top: 30px">确定</el-button>-->
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'CommunicationProtocol',
  data() {
    return {
      info: {
        subjectName: '采集控制',
        date: '2021/05/01',
        version: 'V1.0',
        busType: 'RS232',
        communicationMethod: '点对点',
        refreshCycle: '事件',
      },
      tableData: [
        {
          id: '1',
          name: '帧头',
          describe: '00055',
          options: [
            {
              value: '00056',
              label: '00056',
            },
            {
              value: '00057',
              label: '00057',
            },
            {
              value: '00067',
              label: '00067',
            },
            {
              value: '00068',
              label: '00068',
            },
          ],
        },
        {
          id: '2',
          name: '消息长度',
          describe: '4byte',
        },
        {
          id: '3',
          name: '帧尾',
          describe: '00066',
          options: [
            {
              value: '00056',
              label: '00056',
            },
            {
              value: '00057',
              label: '00057',
            },
            {
              value: '00067',
              label: '00067',
            },
            {
              value: '00068',
              label: '00068',
            },
          ],
        },
      ],
      result: '',
      formInline: {
        name: '采集控制',
        date: '2021/05/01',
        version: 'V1.0',
        type: 'RS232',
        method: '点对点',
        period: '事件',
      },
    }
  },
  methods: {
    frame() {
      this.result = ''
      this.result += this.tableData[2].describe.replace(/\s*/g, '')
      // for (let i = 0; i < this.tableData.length; i++) {
      //   if (i !== 1) this.result += this.tableData[i].describe.replace(/\s*/g, '')
      // }
    },
  },
  mounted() {
    this.frame()
  },
}
</script>

<style scoped></style>
