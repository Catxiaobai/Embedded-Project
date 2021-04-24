<template>
  <div id="item">
    <el-card class="tableTitle">
      <span style="font-size: 20px">当前系统共有{{ total }}个成员</span>
      <el-input v-model="search" placeholder="输入成员姓名搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="primary" style="margin-left: 40%" @click="handleAdd('addForm')" icon="el-icon-plus">添加新成员</el-button>
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
        <el-table-column label="单位" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.team }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleReset(scope.$index, scope.row)">重置密码</el-button>
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
            <!--            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
    <div id="add">
      <el-dialog :close-on-click-modal="false" title="添加新的成员" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
        <el-form :model="addForm" :rules="rules2" ref="addForm">
          <el-form-item label="成员姓名" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入成员姓名"></el-input>
          </el-form-item>
          <el-form-item label="成员账号" label-width="120px" prop="account">
            <el-input v-model="addForm.account" clearable placeholder="请输入用户账号："></el-input>
          </el-form-item>
          <el-form-item label="初始密码" label-width="120px" prop="password">
            <el-input v-model="addForm.password" clearable placeholder="默认初始密码为：666666"></el-input>
          </el-form-item>
          <el-form-item label="成员权限" label-width="120px" prop="level">
            <!--            <el-input v-model="addForm.level" clearable placeholder="请输入成员权限："></el-input>-->
            <el-select v-model="addForm.level" placeholder="请选择权限">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="单位" label-width="120px" prop="password">
            <el-input v-model="addForm.team" clearable placeholder="所属单位"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="edit">
      <el-dialog :close-on-click-modal="false" title="编辑项目" :visible.sync="visible.editDialog" center @close="resetForm('editForm')">
        <el-form :model="editForm" :rules="rules2" ref="editForm">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="editForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="项目介绍" label-width="120px" prop="introduction">
            <el-input v-model="editForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete"></div>
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
      visible: {
        addDialog: false,
        addDialog2: false,
        deleteDialog: false,
        editDialog: false,
        pathInput: false,
      },
      editForm: {
        //修改时使用
        id: '',
        name: '',
        software: '',
        level: '',
        path: '',
        team: '',
      },
      addForm: {
        //添加使用
        name: '',
        account: '',
        level: '',
        password: '666666',
        team: '',
      },
      addForm2: {
        //添加使用
        name: '',
        software: '',
        basedItem: '',
        level: '',
        path: '',
        team: '',
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        software: [{ required: true, message: '不能为空', trigger: 'blur' }],
        team: [{ required: true, message: '不能为空', trigger: 'blur' }],
        level: [{ required: true, message: '不能为空', trigger: 'blur' }],
        path: [{ required: true, message: '不能为空', trigger: 'blur' }],
        basedItem: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
      rules2: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        account: [{ required: true, message: '不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '不能为空', trigger: 'blur' }],
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
          // this.options = []
          // for (let i = 0; i < this.data.length; i++) {
          //   this.options.push({ value: this.data[i].name, label: this.data[i].name })
          // }
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
            .post(this.Global_Api + '/api/add_person', { data: this.addForm, user: this.userInfo })
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('添加成功')
                this.pageList()
              } else {
                console.log(response.data)
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
    handleAddCommit2(formName) {
      console.log(formName)
      // todo: 基于已有项目创建
    },
    handleEditCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/edit_item', this.editForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                // this.$message.success('修改成功')
                this.$message.success('修改成功')
                this.pageList()
              } else {
                this.$message.error(response.data.error_message)
                console.log(response.data)
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          this.visible.editDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleDelete(index, row) {
      console.log(index, row)
      this.$confirm('此操作将删除此成员, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$http
            .post(this.Global_Api + '/api/delete_person', { id: row.id, user: this.userInfo })
            .then((response) => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!',
                })
                this.pageList()
              } else {
                this.$message({
                  type: 'error',
                  message: '删除失败! ' + response.data.error_message,
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
      this.editForm.introduction = row.item_introduction
      this.editForm.name = row.item_name
      this.editForm.id = row.item_id
      this.visible.editDialog = true
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
    handleReset(index, row) {
      console.log(index, row)
      this.$confirm('此操作将重置成员密码为666666, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$http
            .post(this.Global_Api + '/api/reset_person_password', { id: row.id })
            .then((response) => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '重置成功!',
                })
                this.pageList()
              } else {
                this.$message({
                  type: 'error',
                  message: '重置失败!',
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
            message: '已取消重置',
          })
        })
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
