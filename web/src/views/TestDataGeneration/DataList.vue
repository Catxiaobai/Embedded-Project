<template>
  <div>
    <el-card>
      <div>
        <el-row>
          <el-col :span="3">
            <download-excel class="export-excel-wrapper" :data="rawData" :fields="json_fields" name="data" type="xls">
              <el-button type="primary">导出表格</el-button>
            </download-excel>
          </el-col>
          <el-col :span="3">
            <el-button type="primary" @click="generate_script_all">导出脚本</el-button>
          </el-col>
        </el-row>
      </div>
      <el-table
        v-loading="loading"
        element-loading-text="正在生成脚本..."
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        :data="tableData"
        :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
        style="width: 100%; margin-top: 20px"
        @filter-change="filterType"
        height="488px"
        width="100%"
        border
      >
        <el-table-column type="expand" label="详情" width="60">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="TF:">
                <span style="font-weight: normal">{{ props.row.TF }}</span>
              </el-form-item>
              <el-form-item label="测试数据:">
                <span style="font-weight: normal">{{ props.row.data }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <!--        <el-table-column prop="page_id" label="ID" width="60" align="center"></el-table-column>-->
        <el-table-column prop="type" label="类别" width="120" align="center" show-overflow-tooltip column-key="type"> </el-table-column>
        <el-table-column prop="path" label="测试路径" width="200" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="function" label="生成方法" width="120" align="center" show-overflow-tooltip :filters="filters.function" column-key="function">
        </el-table-column>
        <el-table-column prop="data" label="测试数据" show-overflow-tooltip></el-table-column>
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
  name: 'DataList',
  data() {
    return {
      limit: 10, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      loading: false,
      rawData: [],
      tableData: [],
      spanArr: [], //用于存放每一行记录的合并数
      itemInfo: '',
      filters: {
        type: [
          { text: '全迁移', value: '全迁移' },
          { text: '全状态', value: '全状态' },
        ],
        function: [
          { text: '等价类划分', value: '等价类划分' },
          { text: '边界值', value: '边界值' },
          { text: '递增值', value: '递增值' },
          { text: '递减值', value: '递减值' },
          { text: '条件覆盖', value: '条件覆盖' },
          { text: 'MC/DC', value: 'MC/DC' },
          { text: '时序约束', value: '时序约束' },
        ],
      },
      json_fields: {
        类别: 'type',
        测试路径: 'path',
        生成方法: 'function',
        测试数据: 'data',
        状态: 'TF',
      },
      filter: {
        type: [],
        function: [],
      },
    }
  },
  methods: {
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      const dataProvider = this.tableData
      const cellValue = row[column.property]
      if (cellValue) {
        // 上一条数据
        const prevRow = dataProvider[rowIndex - 1]
        // 下一条数据
        let nextRow = dataProvider[rowIndex + 1]
        // 当上一条数据等于下一条数据
        if (prevRow && prevRow[column.property] === cellValue) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let rowspan = 1
          while (nextRow && nextRow[column.property] === cellValue) {
            rowspan++
            nextRow = dataProvider[rowspan + rowIndex]
          }
          if (rowspan > 1) {
            return { rowspan, colspan: 1 }
          }
        }
      }
    },
    pageList() {
      this.$http
        .post(this.Global_Api + '/api/generation/test_data_list', this.itemInfo)
        .then((response) => {
          this.rawData = response.data.test_data_list
          this.data = this.rawData
          console.log(this.rawData)
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
    filterType(value) {
      if (value['function'].length > 0) {
        this.data = []
        for (let i = 0; i < this.rawData.length; i++) {
          if (value['function'].includes(this.rawData[i].function)) {
            this.data.push(this.rawData[i])
          }
        }
      } else {
        this.data = this.rawData
      }
      // if (this.filter['type'] === 0 && this.filter['function'] === 0) {
      //   tempData = temp
      // } else {
      //   for (let k in this.filter) {
      //     if (this.filter[k].length > 0) {
      //       console.log(temp)
      //       for (let i = 0; i < temp.length; i++) {
      //         if (this.filter[k].indexOf(temp[i][k]) > -1) {
      //           tempData.push(temp[i])
      //         }
      //       }
      //       console.log(tempData)
      //       temp = tempData
      //     }
      //   }
      // }

      // for (let k in this.filter) {
      //   if (this.filter[k].length > 0) {
      //     for (let i = 0; i < temp.length; i++) {
      //       console.log(temp[i][k])
      //       console.log(this.filter[k])
      //       if (this.filter[k].includes(temp[i][k])) {
      //         tempData.push(temp[i])
      //       }
      //     }
      //     temp = tempData
      //   } else {
      //     tempData = temp
      //   }
      // }
      this.getList()
    },
    generate_script_all() {
      this.loading = true
      this.$http.post(this.Global_Api + '/api/generation/generate_script_all', { item: this.itemInfo, data: this.rawData }).then((response) => {
        console.log(response.data.path)
        this.loading = false
        // this.$message.success('导出成功')
        this.$notify({
          title: '脚本文件保存路径',
          message: this.$createElement('div', { style: 'word-wrap: break-word;word-break:break-all' }, response.data.path),
          duration: 0,
          position: 'bottom-left',
          type: 'success',
        })
      })
    },
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
}
</script>

<style scoped lang="scss">
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
  font-weight: bold;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 100%;
  font-weight: bold;
}
</style>
