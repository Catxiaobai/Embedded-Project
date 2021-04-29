<template>
  <div id="itemMember">
    <el-card>
      <div id="search">
        <el-input v-model="search" placeholder="按名称搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="actionButton" style="margin-left: 75%; margin-bottom: 20px; margin-top: -30px">
        <el-button type="primary" @click="handleAdd">增加项目成员</el-button>
        <el-button type="danger" :disabled="disabled.delete" @click="ondelclick">删除</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="page_id" label="序号" width="80" align="center"> </el-table-column>
          <el-table-column prop="name" label="姓名" align="center"> </el-table-column>
          <el-table-column prop="account" label="账号" align="center"> </el-table-column>
          <el-table-column prop="level" label="权限" align="center"> </el-table-column>
          <el-table-column prop="team" label="单位" align="center"> </el-table-column>
        </el-table>
      </div>
      <div id="page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[1, 5, 10]"
          :page-size="pagination.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          style="margin-left: 30%; margin-top: 20px"
        >
        </el-pagination>
      </div>
    </el-card>
    <div id="add">
      <el-dialog :close-on-click-modal="false" title="添加项目成员" :visible.sync="visible.addDialog" center>
        <div id="actionButton2">
          <el-button type="primary" :disabled="disabled.add" @click="handleSelect" style="margin-bottom: 10px">选择加入此项目</el-button>
        </div>
        <div id="table2">
          <el-table :data="tableData2" border style="width: 100%" @selection-change="handleSelection2">
            <el-table-column type="selection" width="40px"> </el-table-column>
            <el-table-column prop="page_id" label="序号" width="80" align="center"> </el-table-column>
            <el-table-column prop="name" label="姓名" align="center"> </el-table-column>
            <el-table-column prop="account" label="账号" align="center"> </el-table-column>
            <el-table-column prop="level" label="权限" align="center"> </el-table-column>
            <el-table-column prop="team" label="单位" align="center"> </el-table-column>
          </el-table>
        </div>
        <div id="page2">
          <el-pagination
            @size-change="handleSizeChange2"
            @current-change="handleCurrentChange2"
            :current-page="pagination2.page"
            :page-sizes="[1, 5, 10]"
            :page-size="pagination2.limit"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination2.total"
            style="margin-left: 30%; margin-top: 20px"
          >
          </el-pagination>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog :close-on-click-modal="false" title="删除成员" :visible.sync="visible.deleteDialog" center width="300px">
        <span>是否删除所选成员</span>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleDeleteCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemMember.vue',
  data() {
    return {
      tableData: [],
      tableData2: [],
      pagination: {
        limit: 5, //每页显示条数
        total: 0, //项目总数
        page: 1, //第几页
      },
      pagination2: {
        limit: 5, //每页显示条数
        total: 0, //项目总数
        page: 1, //第几页
      },
      search: '', //搜索框
      search2: '', //搜索框
      visible: {
        addDialog: false,
        deleteDialog: false,
        editDialog: false,
      },
      disabled: {
        edit: true,
        delete: true,
        add: true,
      },
      addForm: {
        //添加使用
        name: '',
        describe: '',
        content: '',
        element: '',
        type: 'sub',
        item_id: '',
      },
      itemInfo: '',
      addData: [],
    }
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  methods: {
    ondelclick() {
      this.visible.deleteDialog = true
    },
    handleSelect() {
      console.log(this.addData)
      console.log(this.itemInfo)
      this.$http
        .post(this.Global_Api + '/api/add_person_to_item', { item: this.itemInfo, data: this.addData })
        .then((response) => {
          if (response.data.error_code === 0) {
            this.$message.success('添加成功')
            this.pageList()
          } else {
            this.$message.error(response.data.error_message)
            this.pageList()
          }
          this.visible.addDialog = false
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .post(this.Global_Api + '/api/item_person_list', this.itemInfo)
        .then((response) => {
          // console.log(response.data.analysis_list)
          this.data = response.data.item_person_list
          console.log(this.data)
          // this.getLevel(this.data)
          this.getList()
        })
        .catch(function (error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    getList() {
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.name.includes(this.search))
      // console.log('list', list)
      this.adjustId(list)
      this.getLevel(list)
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      console.log('this.tableData', this.tableData)
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    adjustId(list) {
      for (let i = 0; i < list.length; i++) {
        list[i].page_id = i + 1
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('子场景项目信息', this.itemInfo)
    },
    handleSizeChange(val) {
      // 当每页数量改变
      console.log(`每页 ${val} 条`)
      this.pagination.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      // 当当前页改变
      console.log(`当前页: ${val}`)
      this.pagination.page = val
      this.getList()
    },
    handleSelection(val) {
      console.log(val)
      if (val.length === 0) {
        this.disabled.delete = true
      } else {
        this.disabled.delete = false
        this.deleteData = val
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleAdd() {
      this.visible.addDialog = true
      // todo: 展示所有未在此项目中的普通成员，可选择加入此项目
      this.pageList2()
    },
    handleAddCommit(formName) {
      this.addForm.type = 'sub'
      this.addForm.item_id = this.itemInfo.id
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/add_scenes', this.addForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('添加成功')
                this.pageList()
              } else {
                this.$message.error(response.data.error_message)
                this.pageList()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          this.visible.addDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleDeleteCommit() {
      console.log(this.deleteData)
      this.$http
        .post(this.Global_Api + '/api/delete_person_from_item', this.deleteData)
        .then((response) => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.$message.success('删除成功')
            this.pageList()
            this.visible.deleteDialog = false
          } else {
            this.$message.error(response.data.error_message)
            this.pageList()
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    pageList2() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .post(this.Global_Api + '/api/normal_person_list', this.itemInfo)
        .then((response) => {
          // console.log(response.data.analysis_list)
          this.data = response.data.normal_person_list
          // 筛选出子场景
          this.getList2()
        })
        .catch(function (error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    getList2() {
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.name.includes(this.search2))
      // console.log('list', list)
      this.adjustId(list)
      // let list = this.data
      this.tableData2 = list.filter(
        (item, index) => index < this.pagination2.page * this.pagination2.limit && index >= this.pagination2.limit * (this.pagination2.page - 1)
      )
      console.log('this.tableData2', this.tableData2)
      this.pagination2.total = list.length
      // console.log(this.tableData)
    },
    handleSizeChange2(val) {
      // 当每页数量改变
      console.log(`每页 ${val} 条`)
      this.pagination2.limit = val
      this.getList2()
    },
    handleCurrentChange2(val) {
      // 当当前页改变
      console.log(`当前页: ${val}`)
      this.pagination2.page = val
      this.getList()
    },
    handleSelection2(val) {
      console.log(val)
      if (val.length === 0) {
        this.disabled.add = true
      } else {
        this.disabled.add = false
        this.addData = val
      }
    },
    getLevel(data) {
      for (let i = 0; i < data.length; i++) {
        if (data[i].authority === 1) {
          data[i].level = '普通成员'
        } else if (data[i].authority === 2) {
          data[i].level = '项目管理员'
        } else if (data[i].authority === 3) {
          data[i].level = '系统管理员'
        }
      }
    },
  },
}
</script>

<style scoped></style>
