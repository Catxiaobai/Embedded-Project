<template>
  <div id="item">
    <el-card class="tableTitle">
      <span style="font-size: 20px">当前系统共有{{ total }}个成员</span>
      <el-input v-model="search" placeholder="输入成员姓名搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <!--      <el-button size="20px" type="primary" style="margin-left: 40%" @click="handleAdd('addForm')" icon="el-icon-plus">添加新成员</el-button>-->
      <el-table :data="tableData" style="width: 100%; margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column label="序号" width="80px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.page_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="姓名" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="账号" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.account }}</span>
          </template>
        </el-table-column>
        <el-table-column label="权限" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.level }}</span>
          </template>
        </el-table-column>
        <!--        <el-table-column label="负责项目数" align="center">-->
        <!--          <template slot-scope="scope">-->
        <!--            <span style="margin-left: 10px">{{ scope.row.level }}</span>-->
        <!--          </template>-->
        <!--        </el-table-column>-->
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <!--            <el-button size="mini" type="success" @click="visibleEdit = true">修改用户权限</el-button>-->
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">修改用户权限</el-button>
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
            <!--            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
            <!--            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>-->
            <!--            <el-popconfirm icon="el-icon-info" iconColor="red" title="确定删除此项目吗？" @confirm="handleDelete(scope.$index, scope.row)">-->
            <!--              <el-button slot="reference" size="mini" type="danger" style="margin-left: 15px">删除</el-button>-->
            <!--            </el-popconfirm>-->
          </template>
        </el-table-column>
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
    <div>
      <el-dialog :close-on-click-modal="false" title="修改权限" :visible.sync="visibleEdit" center @close="resetForm('addForm')">
        <el-form :model="editForm" :rules="rules" ref="addForm">
          <el-form-item label="用户权限" label-width="120px" prop="level">
            <el-select v-model="editForm.level" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit()">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      limit: 10, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [], //项目表
      showItem: {}, //查看项目
      visibleEdit: false,
      visible: {
        addDialog: false,
        addDialog2: false,
        deleteDialog: false,
        editDialog: false,
        pathInput: false,
      },
      editForm: {
        level: '',
        id: '',
        name: '',
      },
      addForm2: {
        //添加使用
        name: '',
        basedItem: '',
        level: '',
        path: '',
        team: '',
      },
      deleteData: [],
      rules: {
        level: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
      options: [
        {
          value: '系统管理员',
          label: '系统管理员',
        },
        {
          value: '项目管理员',
          label: '项目管理员',
        },
        {
          value: '普通成员',
          label: '普通成员',
        },
      ],
      radio: 'false',
      userInfo: '',
    }
  },
  created() {
    this.pageList()
    this.getUserInfo()
  },
  methods: {
    pageList() {
      this.$http
        .get(this.Global_Api + '/api/personnel_list')
        .then((response) => {
          this.data = response.data.personnel_list

          this.getList()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    // 处理数据
    getList() {
      let list = this.data.filter((item, index) => item.name.includes(this.search))
      this.adjustId(list)
      // let list = this.data
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleOpen(index, row) {
      console.log(row)
      this.$store.commit('changeItem', row)
      this.$router.replace('/itemMain')
    },
    handleAdd(formName) {
      this.visible.addDialog = true
    },
    handleAddCommit(formName) {
      // todo: 打开时进入项目出bug
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/add_item', this.addForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('添加成功')
                this.pageList()
                console.log('response.data.item', response.data.item)
                this.$store.commit('changeItem', response.data.item)
                this.$router.replace('/itemMain')
              } else {
                console.log(response.data)
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
    handleAddCommit2(formName) {
      console.log(formName)
      // todo: 基于已有项目创建
    },
    handleDelete(index, row) {
      console.log(index, row)
      this.$confirm('此操作将删除此项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$http
            .post(this.Global_Api + '/api/delete_item', { id: row.id })
            .then((response) => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!',
                })
                this.pageList()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除',
          })
        })
    },
    handleEdit(index, row) {
      console.log(index, row)
      this.editForm.name = row.name
      this.editForm.id = row.id
      this.editForm.level = row.level
      this.visibleEdit = true
    },
    handleEditCommit() {
      this.$http.post(this.Global_Api + '/api/edit_authority', { user: this.userInfo, editForm: this.editForm }).then((response) => {
        console.log(response.data)
        if (response.data.error_code === 0) {
          // this.$message.success('修改成功')
          this.$message.success('修改成功')
          this.pageList()
        } else {
          // this.$message.error(response.data.error_message)
          this.$message.error(response.data.error_message)
          this.pageList()
        }
      })
      this.visibleEdit = false
    },
    handleAddBasedExist(formName) {
      this.visible.addDialog2 = true
    },
    handleSetPath() {
      if (this.radio === 'false') {
        this.visible.pathInput = false
        this.addForm.path = 'Project/Item'
      } else {
        this.visible.pathInput = true
      }
    },
    getUserInfo() {
      this.userInfo = this.$store.state.user
    },
  },
}
</script>

<style lang="scss" scoped>
.tableTitle {
  height: 634px;
  overflow-y: scroll;
}
</style>
