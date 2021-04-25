<template>
  <div id="fullState">
    <el-card>
      <el-table :data="tableData" :span-method="objectSpanMethod" border style="width: 100%; margin-top: 20px">
        <el-table-column prop="id" label="ID" width="80"> </el-table-column>
        <el-table-column prop="type" label="类别" width="180"> </el-table-column>
        <el-table-column prop="case" label="测试路径"> </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)" type="primary">接口协议生成</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="测试数据"> </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'FullState.veu',
  inject: ['reload'],
  data() {
    return {
      tableData: [
        {
          id: 1,
          type: '全状态',
          case: '[t1,t2,t3,t4]',
        },
        {
          id: 2,
          type: '全状态',
          case: '[t5,t6,t7,t8]',
        },
        {
          id: 3,
          type: '全状态',
          case: '[t9,t10,t11,t12]',
        },
        {
          id: 4,
          type: '全迁移',
          case: '[t6,t5,t3,t4]',
        },
        {
          id: 5,
          type: '全迁移',
          case: '[t9,t12,t7,t5]',
        },
      ],
      spanArr: [], //用于存放每一行记录的合并数
    }
  },
  methods: {
    getSpanArr() {
      // data就是我们从后台拿到的数据
      var data = this.tableData
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
        console.log(this.spanArr)
      }
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 1) {
        console.log(row, column, rowIndex, columnIndex)
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        console.log(`rowspan:${_row} colspan:${_col}`)
        return {
          // [0,0] 表示这一行不显示， [2,1]表示行的合并数
          rowspan: _row,
          colspan: _col,
        }
      }
    },
  },
  created() {
    this.getSpanArr()
  },
}
</script>

<style lang="scss" scoped>
.divHelp {
  margin-left: 55%;
  height: 40px;
  margin-top: -40px;
  z-index: 1;
  position: absolute;
}
</style>
