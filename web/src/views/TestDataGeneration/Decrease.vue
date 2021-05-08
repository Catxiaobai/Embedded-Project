<template>
  <div id="fullState">
    <el-card>
      <el-table :data="tableData" :span-method="objectSpanMethod" border style="width: 100%; margin-top: 20px">
        <el-table-column prop="page_id" label="ID" width="80"> </el-table-column>
        <el-table-column prop="type2" label="类别" width="180"> </el-table-column>
        <el-table-column prop="path" label="测试路径"> </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="generateDecrease(scope.$index, scope.row)" type="primary">递减值生成</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="测试数据"> </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 5, 10]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 30%; margin-top: 30px"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'FullState.veu',
  inject: ['reload'],
  data() {
    return {
      limit: 10, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      tableData: [],
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
    generateDecrease(index, row) {
      console.log(index, row)
      this.$http
        .post(this.Global_Api + '/api/generation/generate_decrease', { info: row })
        .then((response) => {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    pageList() {
      this.$http
        .get(this.Global_Api + '/api/generation/path_list')
        .then((response) => {
          this.data = response.data.path_list
          this.options = []
          for (let i = 0; i < this.data.length; i++) {
            this.options.push({ value: this.data[i].name, label: this.data[i].name })
          }

          this.getList()
          this.getSpanArr()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    // 处理数据
    getList() {
      // let list = this.data.filter((item, index) => item.name.includes(this.search))
      // this.adjustId(list)
      let list = this.data
      this.adjustId(list)
      this.tableData = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
    },
    adjustId(list) {
      for (let i = 0; i < list.length; i++) {
        list[i].page_id = i + 1
      }
    },
    // 当每页数量改变
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.limit = val
      this.getList()
    },
    // 当当前页改变
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.getList()
    },
  },
  created() {
    this.pageList()
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
