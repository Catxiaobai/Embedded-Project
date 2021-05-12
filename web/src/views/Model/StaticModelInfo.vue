<template>
  <div>
    <el-card style="height: 634px">
      <el-table :data="tableData" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"> </el-table-column>
        <el-table-column prop="part" label="部分" width="180"> </el-table-column>
        <el-table-column prop="details" label="详情"> </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="gotoTest">CAN接口</el-button>
            <el-button size="mini" type="primary" @click="gotoTest(scope.$index, scope.row)">RS232接口</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'StaticModelInfo.vue',
  data() {
    return {
      tableData: [
        {
          id: '1',
          part: '相机部分',
          details: '28335芯片',
        },
        {
          id: '2',
          part: '光学组件部分',
          details: '温控组件',
        },
        {
          id: '3',
          part: '光学组件部分',
          details: '位/俯角控制组件',
        },
        {
          id: '4',
          part: '光学组件部分',
          details: '补偿镜控制组件',
        },
        {
          id: '5',
          part: '光学组件部分',
          details: '检调光控制组件',
        },
        {
          id: '6',
          part: '光学组件部分',
          details: '检调焦控制组件',
        },
        {
          id: '6',
          part: '光学组件部分',
          details: '可见光/红外成像组件',
        },
        {
          id: '7',
          part: '综合显控部分',
          details: '上位机',
        },
      ],
      spanArr: [],
    }
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      }
      return ''
    },
    getSpanArr(data) {
      // data就是我们从后台拿到的数据
      this.spanArr = []
      for (var i = 0; i < data.length; i++) {
        if (i === 0) {
          this.spanArr.push(1)
          this.pos = 0
        } else {
          // 判断当前元素与上一个元素是否相同
          if (data[i].type === data[i - 1].type) {
            this.spanArr[this.pos] += 1
            this.spanArr.push(0)
          } else {
            this.spanArr.push(1)
            this.pos = i
          }
        }
        // console.log(this.spanArr)
      }
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 1) {
        // console.log(row, column, rowIndex, columnIndex)
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        // console.log(`rowspan:${_row} colspan:${_col}`)
        return {
          // [0,0] 表示这一行不显示， [2,1]表示行的合并数
          rowspan: _row,
          colspan: _col,
        }
      }
    },
    gotoTest() {
      this.$router.replace('/communicationProtocol')
    },
  },
  mounted() {
    this.getSpanArr(this.tableData)
  },
}
</script>

<style scoped></style>
