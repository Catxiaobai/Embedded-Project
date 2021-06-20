<template>
  <div>
    <el-card>
      <el-button type="primary" @click="addDialog = true"> 添加通信协议 </el-button>
      <el-divider></el-divider>
      <el-table :data="tableData" style="width: 100%; margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column prop="page_id" label="序号" width="60" align="center"> </el-table-column>
        <el-table-column label="接口名称" width="120px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.subject_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="类型" align="center" width="120px">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.type }}</span>
          </template>
        </el-table-column>
        <el-table-column label="通讯方式" align="center" width="120px">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.communication_method }}</span>
          </template>
        </el-table-column>
        <el-table-column label="日期" width="120px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.date }}</span>
          </template>
        </el-table-column>
        <el-table-column label="版本" align="center" width="100px">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.version }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleGoto(scope.$index, scope.row)">配置</el-button>
            <el-button size="mini" type="success" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
      <div id="editDialog">
        <el-dialog :close-on-click-modal="false" title="修改协议" :visible.sync="editDialog" center width="800px">
          <el-form :model="editForm" :rules="rules" ref="editForm" label-width="100px">
            <el-row>
              <el-col :span="8">
                <el-form-item label="主题名称" prop="subject_name">
                  <el-input v-model="editForm.subject_name" placeholder="请填写主题名称"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="类型" prop="type">
                  <el-input v-model="editForm.type" placeholder="请填写类型"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="日期" prop="date">
                  <el-input v-model="editForm.date" placeholder="请填写日期"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="通讯方式" prop="communication_method">
                  <el-input v-model="editForm.communication_method" placeholder="请填写通讯方式"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="版本" prop="version">
                  <el-input v-model="editForm.version" placeholder="请填写版本"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
          </div>
        </el-dialog>
      </div>
      <div id="addDialog">
        <el-dialog :close-on-click-modal="false" title="添加协议" :visible.sync="addDialog" center width="800px">
          <el-form :model="addForm" :rules="rules" ref="addForm" label-width="100px">
            <el-row>
              <el-col :span="8">
                <el-form-item label="接口名称" prop="subject_name">
                  <el-input v-model="addForm.subject_name" placeholder="请填写接口名称"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="类型" prop="type">
                  <el-select v-model="addForm.type" placeholder="请选择">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="日期" prop="date">
                  <el-input v-model="addForm.date" placeholder="请填写日期"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="通讯方式" prop="communication_method">
                  <el-input v-model="addForm.communication_method" placeholder="请填写通讯方式"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="版本" prop="version">
                  <el-input v-model="addForm.version" placeholder="请填写版本"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
          </div>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ShowEdit',
  data() {
    return {
      limit: 10, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      tableData: '', //项目表
      itemInfo: '',
      editDialog: false,
      addDialog: false,
      editForm: {
        subject_name: '',
        date: '',
        version: '',
        type: '',
        communication_method: '',
        refresh_cycle: '',
        item_id: '',
      },
      addForm: {
        subject_name: '',
        date: '',
        version: '',
        type: '',
        communication_method: '',
        refresh_cycle: '',
        item_id: '',
      },
      options: [
        {
          value: '总线量',
          label: '总线量',
        },
        {
          value: '离散量',
          label: '离散量',
        },
        {
          value: '枚举值',
          label: '枚举值',
        },
        {
          value: '模拟量',
          label: '模拟量',
        },
      ],
      rules: {
        subject_name: [{ required: true, message: '请填写主题名称', trigger: 'blur' }],
        date: [{ required: true, message: '请填写日期', trigger: 'blur' }],
        version: [{ required: true, message: '请填写版本', trigger: 'blur' }],
        type: [{ required: true, message: '请填写类型', trigger: 'blur' }],
        communication_method: [{ required: true, message: '请填写通讯方式', trigger: 'blur' }],
        refresh_cycle: [{ required: true, message: '请填写刷新周期', trigger: 'blur' }],
      },
    }
  },
  methods: {
    pageList() {
      this.$http
        .post(this.Global_Api + '/api/generation/protocol_list', this.itemInfo)
        .then((response) => {
          this.rawData = response.data.protocol_list
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
      this.addForm.item_id = this.itemInfo.id
    },
    handleDelete(index, row) {
      console.log(index, row)
      this.$confirm('此操作将删除此协议, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$http
            .post(this.Global_Api + '/api/generation/delete_protocol', { id: row.id })
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
                  message: '删除失败!',
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
      this.editDialog = true
      this.editForm = row
    },
    handleEditCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/generation/edit_protocol', this.editForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('修改成功')
                this.pageList()
              } else {
                this.$message.error(response.data.error_message)
                this.pageList()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          this.editDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleAddCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/generation/add_protocol', this.addForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('添加成功')
                this.pageList()
                this.$refs[formName].resetFields()
              } else {
                this.$message.error(response.data.error_message)
                console.log(response.data)
                this.pageList()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          this.addDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleGoto(index, row) {
      console.log(index, row)
      this.$store.commit('setProtocol', row)
      this.$router.replace('/deploy')
    },
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
}
</script>

<style scoped></style>
