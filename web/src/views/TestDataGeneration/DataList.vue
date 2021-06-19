<template>
  <div>
    <el-card>
      <el-table
        height="610"
        width="100%"
        border
        :data="tableData"
        :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
        :summary-method="getSummaries"
        show-summary
        :default-sort="{ prop: 'page_id' }"
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
        <el-table-column prop="page_id" label="ID" width="40" align="center"></el-table-column>
        <el-table-column prop="type" label="类别" width="120" align="center" show-overflow-tooltip :filters="filters.type" :filter-method="filterType">
        </el-table-column>
        <el-table-column prop="path" label="测试路径" width="200" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column
          prop="function"
          label="生成方法"
          width="120"
          align="center"
          show-overflow-tooltip
          :filters="filters.function"
          :filter-method="filterFunction"
        >
        </el-table-column>
        <el-table-column prop="data" label="测试数据" show-overflow-tooltip></el-table-column>
        <!--        <el-table-column prop="script" label="脚本生成" align="center" width="102">-->
        <!--          <template slot-scope="scope">-->
        <!--            <el-button type="primary" size="small" @click="gotoLink(scope.row)">脚本生成</el-button>-->
        <!--          </template>-->
        <!--        </el-table-column>-->
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'DataList',
  data() {
    return {
      tableData: [
        {
          page_id: 1,
          type: 'type',
          path: 'path',
          function: 'function',
          data: 1,
        },
      ],
      spanArr: [], //用于存放每一行记录的合并数
      total: 0,
      itemInfo: '',
      filters: {
        type: [
          { text: '全迁移', value: '全迁移' },
          { text: '全状态', value: '全状态' },
        ],
        function: [
          { text: '随机值', value: '随机值' },
          { text: '边界值', value: '边界值' },
          { text: '递增值', value: '递增值' },
          { text: '递减值', value: '递减值' },
          { text: '条件覆盖', value: '条件覆盖' },
          { text: 'MC/DC', value: 'MC/DC' },
        ],
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
    generateBoundary(index, row) {
      console.log(index, row)
      this.loading = true
      this.$http
        .post(this.Global_Api + '/api/generation/generate_boundary', row)
        .then((response) => {
          this.loading = false
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
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
      this.tableData = list
    },
    adjustId(list) {
      for (let i = 0; i < list.length; i++) {
        list[i].page_id = i + 1
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    filterType(value, row, column) {
      console.log(value, row, column)
      return row['type'] === value
    },
    filterFunction(value, row) {
      return row['function'] === value
    },
    getSummaries(param) {
      const { columns, data } = param
      const sums = []
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = '统计'
          return
        }
        if (index === 5) {
          sums[index] = '共 ' + data.length + ' 条数据'
          return
        }
      })

      return sums
    },
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  watch: {
    tableData() {
      this.total = this.tableData.length
    },
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
