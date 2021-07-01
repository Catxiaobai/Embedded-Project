<template>
  <div id="fullState">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="3">
          <el-button type="primary" style="margin-left: 20px" @click="GenerateAllData">一键生成</el-button>
        </el-col>
        <el-col :span="20">
          <el-progress :percentage="percentage" :format="format(percent, percentTotal)" style="margin-top: 10px"></el-progress>
        </el-col>
      </el-row>
      <el-table
        v-loading="loading"
        element-loading-text="数据生成中..."
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        :data="tableData"
        :span-method="objectSpanMethod"
        border
        style="width: 100%; margin-top: 20px"
        @filter-change="filterType"
        height="488px"
      >
        <el-table-column prop="page_id" label="ID" width="40"> </el-table-column>
        <el-table-column prop="type2" label="类别" width="80" :filters="filterItem"> </el-table-column>
        <el-table-column prop="path" label="测试路径"> </el-table-column>
        <el-table-column prop="amount" label="规模" width="100">
          <template slot-scope="scope">
            <el-input v-model="scope.row.amount" class="tableCell"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="114">
          <template slot-scope="scope">
            <el-button size="mini" @click="generateDecrease(scope.$index, scope.row)" type="primary">递减值生成</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="测试数据" width="100">
          <template slot-scope="scope">
            <el-link @click="gotoShow(scope.row)">data</el-link>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 5, 10, 1000]"
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
      itemInfo: '',
      loading: false,
      filterItem: [
        { text: '全状态', value: '全状态' },
        { text: '全迁移', value: '全迁移' },
      ],
      options: [],
      percentTotal: 20,
      percent: 0,
      percentage: 0,
    }
  },
  methods: {
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
    generateDecrease(index, row) {
      console.log(index, row)
      this.loading = true
      this.$http
        .post(this.Global_Api + '/api/generation/generate_decrease', row)
        .then((response) => {
          this.loading = false
          this.gotoShow(row)
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    pageList() {
      this.$http
        .post(this.Global_Api + '/api/generation/path_list', this.itemInfo)
        .then((response) => {
          this.rawData = response.data.path_list
          this.percentTotal = this.rawData.length
          for (let i = 0; i < this.rawData.length; i++) {
            this.rawData[i].time = 0
            this.rawData[i].amount = 1
          }
          this.data = this.rawData
          this.getList()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    // 处理数据
    getList() {
      let list = this.data
      this.adjustId(list)
      this.tableData = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
      this.getSpanArr(this.tableData)
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
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    gotoShow(row) {
      row['name'] = '递减值'
      console.log('test', row)
      this.$store.commit('setPath', row)
      this.$router.replace('/dataShow')
    },
    filterType(value) {
      let key = ''
      for (key in value) {
        console.log(value[key])
      }
      if (value[key].length === 1) {
        this.data = []
        for (let i = 0; i < this.rawData.length; i++) {
          if (this.rawData[i].type2 === value[key][0]) {
            this.data.push(this.rawData[i])
          }
        }
      } else {
        this.data = this.rawData
      }
      this.getList()
    },
    getProtocol() {
      this.$http
        .post(this.Global_Api + '/api/generation/protocol_list', this.itemInfo)
        .then((response) => {
          console.log(response.data.protocol_list)
          let temp_data = response.data.protocol_list
          for (let i = 0; i < temp_data.length; i++) {
            let temp_dict = { value: temp_data[i]['subject_name'], label: temp_data[i]['subject_name'] }
            this.options.push(temp_dict)
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    GenerateAllData() {
      this.percent = 0
      this.loading = true
      for (let i = 0; i < this.percentTotal; i++) {
        // clearTimeout(this.timer) //清除延迟执行
        setTimeout(() => {
          this.percent = i + 1
          this.percentage = (this.percent / this.percentTotal) * 100
          //设置延迟执行
          this.$http.post(this.Global_Api + '/api/generation/generate_decrease', this.rawData[i]).then((response) => {
            console.log(response.data)
          })
        }, 3000 * i)
      }
    },
    format(percent, percentTotal) {
      return () => {
        return percent.toString() + ' / ' + percentTotal.toString()
      }
    },
  },
  created() {
    this.getItemInfo()
    this.pageList()
    this.getProtocol()
  },
  watch: {
    percent(val) {
      console.log(val)
      if (val === this.percentTotal) this.loading = false
    },
  },
}
</script>

<style scoped></style>
<style lang="scss">
.tableCell {
  .el-textarea__inner {
    border: none;
    resize: none;
  }
}
</style>
