<template>
  <div id="dataShow">
    <el-card>
      <el-table :data="tableData" :span-method="objectSpanMethod" border width="100%">
        <el-table-column prop="page_id" label="ID" width="40" align="center"></el-table-column>
        <el-table-column prop="type2" label="类别" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="生成方法" width="80" align="center"></el-table-column>
        <el-table-column v-for="(item, index) in desCol_mcdc" :prop="item.prop" :label="item.label" :key="index" align="center"></el-table-column>
        <el-table-column prop="path" label="测试路径" width="280" align="center">
          <el-table-column v-for="(item, index) in desCol" :prop="item.prop" :label="item.label" :key="index" align="center"></el-table-column>
        </el-table-column>
        <el-table-column prop="script" label="脚本生成" align="center" width="102">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="gotoLink(scope.row)">脚本生成</el-button>
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
  name: 'DataShow.vue',
  data() {
    return {
      limit: 10, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      itemInfo: '',
      pathInfo: '',
      spanArr: [],
      tableData: [],
      desCol: [],
      desCol_mcdc: [],
      aimPath: '',
      param: '',
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
      if (columnIndex === 1 || columnIndex === 2) {
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
    pageList() {
      this.$http
        .post(this.Global_Api + '/api/generation/data_list', this.pathInfo)
        .then((response) => {
          this.rawData = response.data.data_list
          console.log(this.rawData[0])
          if (this.rawData[0].name === '随机值') {
            this.dataList(this.rawData[0].data)
          } else if (this.rawData[0].name === 'MC/DC' || this.rawData[0].name === '条件覆盖') {
            this.dataList3(this.rawData[0].data)
          } else {
            this.dataList2(this.rawData[0].data)
          }

          this.getList()
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
    getPathInfo() {
      this.pathInfo = this.$store.state.path
    },
    columnList() {
      this.aimPath = eval(this.pathInfo.path)
      console.log(this.aimPath)
      this.desCol = []
      for (let i = 0; i < this.aimPath.length; i++) {
        this.desCol.push({ prop: this.aimPath[i], label: this.aimPath[i] + '(' + this.param[this.aimPath[i]] + ')' })
      }
    },
    dataList(data) {
      data = eval('(' + data + ')') //神奇
      this.data = []
      console.log(data)
      for (let key in data) {
        if (key !== 'name') {
          let temp = {
            id: this.rawData[0].id,
            path_id: this.rawData[0].path_id,
            item_id: this.rawData[0].item_id,
            name: this.rawData[0].name,
            type2: this.rawData[0].type2,
          }

          for (let i = 0; i < this.aimPath.length; i++) {
            temp[this.aimPath[i]] = data[key][this.aimPath[i]]
          }
          this.data.push(temp)
          console.log(this.data)
        }
      }
    },
    dataList2(data) {
      data = eval('(' + data + ')') //神奇
      this.data = []
      console.log(data)
      let max_len = data[this.aimPath[0]].length
      for (let i = 0; i < this.aimPath.length; i++) {
        max_len = Math.max(max_len, data[this.aimPath[i]].length)
      }
      for (let i = 0; i < max_len; i++) {
        let temp = {
          id: this.rawData[0].id,
          path_id: this.rawData[0].path_id,
          item_id: this.rawData[0].item_id,
          name: this.rawData[0].name,
          type2: this.rawData[0].type2,
        }
        for (let j = 0; j < this.aimPath.length; j++) {
          temp[this.aimPath[j]] = data[this.aimPath[j]][i]
        }
        this.data.push(temp)
      }
      console.log(this.data)
    },
    dataList3(data) {
      data = eval('(' + data + ')') //神奇
      this.data = []
      console.log(data)
      this.desCol_mcdc.push({ prop: 'TF', label: 'TF' })
      for (let key in data) {
        if (key !== 'name') {
          let temp = {
            id: this.rawData[0].id,
            path_id: this.rawData[0].path_id,
            item_id: this.rawData[0].item_id,
            name: this.rawData[0].name,
            type2: this.rawData[0].type2,
          }
          temp['TF'] = key
          for (let i = 0; i < data[key].length; i++) {
            temp[this.aimPath[i]] = data[key][i]
          }
          this.data.push(temp)
        }
      }
    },
    gotoLink(row) {
      console.log('test', row)
      this.$store.commit('setScriptData', row)
      this.$router.replace('/script')
    },
    getParameter() {
      this.$http
        .get(this.Global_Api + '/api/generation/get_parameter')
        .then((response) => {
          console.log(response.data.parameter)
          this.param = response.data.parameter
          this.columnList()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
  },
  created() {
    this.getItemInfo()
    this.getParameter()
    this.getPathInfo()
    // this.columnList()
    this.pageList()
  },
}
</script>

<style scoped></style>
<style lang="scss"></style>
