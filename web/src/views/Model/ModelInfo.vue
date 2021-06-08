<template>
  <div id="complexSceneInfo">
    <el-card>
      <div id="search">
        <el-input v-model="search" placeholder="按名称搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="downloadType" style="display: flex; margin-left: 60%; margin-top: -30px">
        <a href="/样例文本.txt" download="样例文本.txt" style="color: #38b2ff; margin-right: 5px">样例文本下载</a>
        |
        <el-upload :action="doUpload" :on-success="handleImport" :show-file-list="false">
          <a style="color: #38b2ff; margin-left: 5px">导入</a>
        </el-upload>
      </div>
      <div id="actionButton" style="margin-left: 75%; margin-bottom: 20px; margin-top: -30px">
        <el-button type="primary" @click="handleAdd('addForm')">添加</el-button>
        <el-button type="success" :disabled="disabled.edit" @click="visible.editDialog = true">编辑</el-button>
        <el-button type="danger" :disabled="disabled.delete" @click="visible.deleteDialog = true">删除</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection" @filter-change="handleFilterChange">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="page_id" label="序号" width="80"> </el-table-column>
          <!--          <el-table-column prop="element" label="类别" width="120" :filters="filterData" column-key="element">-->
          <!--          </el-table-column>-->
          <el-table-column prop="name" label="名称" width="180"> </el-table-column>
          <el-table-column prop="describe" label="描述" :show-overflow-tooltip="true">
            <!--todo: 过长不好看-->
          </el-table-column>
          <el-table-column prop="content" label="规格化表示" width="280" :show-overflow-tooltip="true"> </el-table-column>
        </el-table>
      </div>
      <div id="page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[1, 5, 10, 1000]"
          :page-size="pagination.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          style="margin-left: 30%; margin-top: 20px"
        >
        </el-pagination>
      </div>
    </el-card>
    <!--    <div id="show"></div>-->
    <div id="add">
      <el-dialog :close-on-click-modal="false" title="添加新的场景" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
        <el-form :model="addForm" :rules="rules" ref="addForm">
          <el-form-item label="类别" label-width="120px" prop="element">
            <el-select v-model="addForm.element" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="规格化描述" label-width="120px" prop="content">
            <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="edit">
      <el-dialog :close-on-click-modal="false" title="编辑场景" :visible.sync="visible.editDialog" center>
        <el-form :model="editForm" :rules="rules" ref="editForm">
          <el-form-item label="要素" label-width="120px" prop="element">
            <el-select v-model="editForm.element" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="editForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="editForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="规格化描述" label-width="120px" prop="content">
            <el-input v-model="editForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog :close-on-click-modal="false" title="删除场景" :visible.sync="visible.deleteDialog" center width="300px">
        <span>是否删除所选场景</span>
        <!--        <el-card style="margin-top: 10px">-->
        <!--          <el-table :data="deleteData" border>-->
        <!--            <el-table-column property="id" label="序号" width="50"></el-table-column>-->
        <!--            <el-table-column property="element" label="要素" width="150"></el-table-column>-->
        <!--            <el-table-column property="name" label="名称"></el-table-column>-->
        <!--          </el-table>-->
        <!--        </el-card>-->
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleDeleteCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="upload"></div>
  </div>
</template>

<script>
export default {
  name: 'ModelInfo.vue',
  data() {
    return {
      tableData: [],
      doUpload: this.Global_Api + '/api/upload_file',
      filterData: [
        { text: '外部交联环境', value: '外部交联环境' },
        { text: '功能处理', value: '功能处理' },
        { text: '功能层次', value: '功能层次' },
        { text: '状态迁移', value: '状态迁移' },
      ],
      pagination: {
        limit: 10, //每页显示条数
        total: 0, //项目总数
        page: 1, //第几页
      },
      search: '', //搜索框
      visible: {
        addDialog: false,
        deleteDialog: false,
        editDialog: false,
      },
      disabled: {
        edit: true,
        delete: true,
      },
      editForm: {
        //修改时使用
        id: '',
        name: '',
        type: '',
        describe: '',
        content: '',
        element: '',
      },
      addForm: {
        //添加使用
        name: '',
        describe: '',
        content: '',
        element: '',
        type: 'complex',
        item_id: '',
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }],
        element: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
      options: [
        {
          value: '外部交联环境',
          label: '外部交联环境',
        },
        {
          value: '功能处理',
          label: '功能处理',
        },
        {
          value: '功能层次',
          label: '功能层次',
        },
        {
          value: '状态迁移',
          label: '状态迁移',
        },
      ],
      itemInfo: '',
    }
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .post(this.Global_Api + '/api/scenes_list', this.itemInfo)
        .then((response) => {
          // console.log(response.data.analysis_list)
          this.data = response.data.scenes_list
          // 筛选出子场景
          this.data = this.data.filter((item, index) => item.type.includes('complex'))
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
      this.adjustId(list)
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    adjustId(list) {
      for (let i = 0; i < list.length; i++) {
        list[i].page_id = i + 1
      }
    },
    handleFilterChange(value) {
      console.log(value)
      if (value['element']) {
        this.filterSearch = value['element']
        let list = []
        if (this.filterSearch.length === 0) list = this.data.filter((item, index) => item.element.includes(this.filterSearch))
        for (let i = 0; i < this.filterSearch.length; i++) {
          let temp = this.data.filter((item, index) => item.element.includes(this.filterSearch[i]))
          list = list.concat(temp)
        }
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
      if (value['type']) {
        this.filterSearch = value['type']
        let list = []
        if (this.filterSearch.length === 0) list = this.data.filter((item, index) => item.type.includes(this.filterSearch))
        for (let i = 0; i < this.filterSearch.length; i++) {
          let temp = this.data.filter((item, index) => item.type.includes(this.filterSearch[i]))
          list = list.concat(temp)
        }
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
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
      // 编辑按钮
      if (val.length === 1) {
        this.disabled.edit = false
        this.editForm = val[0]
      } else {
        this.disabled.edit = true
      }
      // 删除按钮
      if (val.length === 0) {
        this.disabled.delete = true
      } else {
        this.disabled.delete = false
        this.deleteData = val
      }
    },
    handleAdd(formName) {
      this.visible.addDialog = true
    },
    handleAddCommit(formName) {
      this.addForm.type = 'complex'
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
    handleEditCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/edit_scenes', this.editForm)
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
          this.visible.editDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleDeleteCommit() {
      this.$http
        .post(this.Global_Api + '/api/delete_scenes', this.deleteData)
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
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('综合场景项目信息', this.itemInfo)
    },
    handleImport(code, file) {
      console.log('test')
      this.$http
        .post(this.Global_Api + '/api/import_scenes', { name: file.name, type: 'complex', item: this.itemInfo })
        .then((response) => {
          if (response.data.error_code === 0) {
            console.log(response)
            this.$message.success('导入成功')
            this.pageList()
          } else {
            // console.log(response.data)
            this.$message.error(response.data.error_message)
            this.pageList()
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
  },
}
</script>

<style lang="scss">
.el-tooltip__popper {
  max-width: 30%;
  line-height: 130%;
  //overflow: hidden;
  display: block;
  white-space: pre-line;
}
</style>
