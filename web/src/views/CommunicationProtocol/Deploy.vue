<template>
  <div>
    <div class="main">
      <el-card class="table" style="height: 653px">
        当前协议：
        <el-select v-model="frame" placeholder="请选择协议" @change="getCurrentProtocol">
          <el-option v-for="item in optionsProtocol" :key="item.value" :label="item.label" :value="item.value"> </el-option>
        </el-select>

        <el-divider></el-divider>
        <el-row :gutter="5">
          <el-col :span="12" class="tableVariable">
            <el-row type="flex" align="middle">
              可选变量列表：
              <el-button type="primary" @click="addDialog = true" style="margin-left: 60%" size="mini"> 添加新变量 </el-button>
            </el-row>
            <el-row type="flex" align="middle" style="margin-top: 10px">
              <el-card style="width: 100%; height: 410px">
                <el-table :data="tableVariable" border height="366" width="100%" @selection-change="toRightChange">
                  <el-table-column type="selection" width="40"> </el-table-column>
                  <!--                  <el-table-column prop="name" label="名称"> </el-table-column>-->
                  <el-table-column prop="describe" label="名称" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="type" label="类型" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="lower_bound" label="下限" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="upper_bound" label="上限" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="value" label="值" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="length" label="长度" show-overflow-tooltip> </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-row>
          </el-col>
          <el-col :span="2" class="handleTransfer">
            <el-row type="flex" align="middle" justify="center"> handle </el-row>
            <el-row type="flex" align="middle" justify="center" style="margin-top: 20px">
              <el-card style="height: 410px">
                <el-button type="primary" style="margin-top: 120px" :disabled="disabled.to_right" @click="toRight">→</el-button>
                <el-row type="flex" align="middle" justify="center" style="margin-top: 30px">
                  <el-button type="primary" :disabled="disabled.to_left" @click="toLeft">←</el-button>
                </el-row>
              </el-card>
            </el-row>
          </el-col>
          <el-col :span="10" class="tableSelect">
            <el-row type="flex" align="middle"> 已选变量列表： </el-row>
            <el-row type="flex" align="middle" style="margin-top: 20px">
              <el-card style="width: 100%; height: 410px">
                <el-table :data="tableSelect" border width="100%" height="366" @selection-change="toLeftChange">
                  <el-table-column type="selection" width="40"> </el-table-column>
                  <el-table-column prop="describe" label="名称" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="type" label="类型" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="lower_bound" label="下限" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="upper_bound" label="上限" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="value" label="值" show-overflow-tooltip> </el-table-column>
                  <el-table-column prop="length" label="长度" show-overflow-tooltip> </el-table-column>
                </el-table>
              </el-card>
            </el-row>
          </el-col>
        </el-row>
        <div style="margin-left: 90%; margin-top: 10px">
          <el-button type="primary" :disabled="disabled.commit" @click="handleSave">保存</el-button>
        </div>
      </el-card>
    </div>
    <div class="dialog">
      <el-dialog :close-on-click-modal="false" title="添加变量" :visible.sync="addDialog" center width="350px">
        <el-form :model="addForm" :rules="rules" ref="addForm" label-width="50px">
          <el-form-item label="标识" prop="name">
            <el-input v-model="addForm.name" placeholder="请填写英文标识"></el-input>
          </el-form-item>
          <el-form-item label="名称" prop="describe">
            <el-input v-model="addForm.describe" placeholder="请填写名称"></el-input>
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="addForm.type" placeholder="请选择" @change="selectType">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="下限" prop="lower_bound" :hidden="hidden.lower_bound">
            <el-input v-model="addForm.lower_bound" placeholder="请填写下限"></el-input>
          </el-form-item>
          <el-form-item label="上限" prop="upper_bound" :hidden="hidden.upper_bound">
            <el-input v-model="addForm.upper_bound" placeholder="请填写上限"></el-input>
          </el-form-item>
          <el-form-item label="值" prop="value" :hidden="hidden.value">
            <el-input v-model="addForm.value" placeholder="格式['value1','value2','value3']"></el-input>
          </el-form-item>
          <el-form-item label="长度" prop="length" :hidden="hidden.length">
            <el-input v-model="addForm.length" placeholder="长度以字节为单位"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Deploy',
  inject: ['reload'],
  data() {
    return {
      tableVariable: [],
      tableSelect: [],
      addForm: {
        name: '',
        describe: '',
        type: '',
        lower_bound: 'None',
        upper_bound: 'None',
        value: 'None',
        length: 'None',
      },
      addDialog: false,
      options: [
        {
          value: 'CONSTANT',
          label: 'CONSTANT',
        },
        {
          value: 'ENUM',
          label: 'ENUM',
        },
        {
          value: 'INT8',
          label: 'INT8',
        },
        {
          value: 'INT16',
          label: 'INT16',
        },
        {
          value: 'INT32',
          label: 'INT32',
        },
        {
          value: 'FLOAT',
          label: 'FLOAT',
        },
        // {
        //   value: 'DOUBLE',
        //   label: 'DOUBLE',
        // },
      ],
      frame: '',
      optionsProtocol: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }],
        // upper_bound: [{ required: true, message: '不能为空', trigger: 'blur' }],
        // lower_bound: [{ required: true, message: '不能为空', trigger: 'blur' }],
        value: [
          // { required: true, message: '不能为空', trigger: 'blur' },
          { pattern: /(^$)|([[](.+?)[\]])|(None)/g, message: '格式：["value1","value2","value3"]', trigger: 'blur' },
        ],
        // length: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
      disabled: {
        to_left: true,
        to_right: true,
        commit: true,
      },
      select: {
        to_right: [],
        to_left: [],
      },
      hidden: {
        lower_bound: true,
        upper_bound: true,
        value: true,
        length: true,
      },
    }
  },
  methods: {
    getItemInfo() {
      this.frame = this.$store.state.protocol.subject_name
      this.itemInfo = this.$store.state.item
      this.addForm.item_id = this.itemInfo.id
    },
    handleAddCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/generation/add_variable', this.addForm)
            .then((response) => {
              if (response.data.error_code === 0) {
                // console.log(this.addForm)
                this.$message.success('添加成功')
                this.reload()
              } else {
                this.$message.error(response.data.error_message)
                this.reload()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          this.addDialog = false
          this.$refs[formName].resetFields()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleDelete(index, row) {
      console.log(index, row)
      this.$confirm('此操作将删除此变量, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$http
            .post(this.Global_Api + '/api/generation/delete_variable', { id: row.id })
            .then((response) => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!',
                })
                this.reload()
              } else {
                this.$message({
                  type: 'error',
                  message: '删除失败!',
                })
                this.reload()
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
    handleSave() {
      console.log(this.tableSelect)
      this.$http
        .post(this.Global_Api + '/api/generation/protocol_save', { protocol: this.frame, variable: this.tableSelect, item_id: this.itemInfo.id })
        .then((response) => {
          console.log(response.data)
          this.$message.success('配置成功')
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    pageList() {
      this.$http
        .post(this.Global_Api + '/api/generation/variable_list', this.itemInfo)
        .then((response) => {
          this.rawData = response.data.variable_list
          this.tableVariable = this.rawData
          console.log(response.data)
          this.getCurrentProtocol()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    toRightChange(val) {
      console.log(val)
      this.select.to_right = val
      if (val.length === 0) this.disabled.to_right = true
      if (val.length !== 0) this.disabled.to_right = false
    },
    toLeftChange(val) {
      console.log(val)
      this.select.to_left = val
      if (val.length === 0) this.disabled.to_left = true
      if (val.length !== 0) this.disabled.to_left = false
    },
    toRight() {
      this.tableSelect.push.apply(this.tableSelect, this.select.to_right)
      // console.log(this.rawData)
      // this.tableVariable = this.rawData.filter((el) => !this.tableSelect.includes(el))
      for (let i = 0; i < this.select.to_right.length; i++) {
        this.tableVariable.splice(this.tableVariable.indexOf(this.select.to_right[i]), 1)
      }
    },
    toLeft() {
      this.tableVariable.push.apply(this.tableVariable, this.select.to_left)
      // this.tableSelect = this.rawData.filter((el) => !this.tableVariable.includes(el))
      for (let i = 0; i < this.select.to_left.length; i++) {
        this.tableSelect.splice(this.tableSelect.indexOf(this.select.to_left[i]), 1)
      }
      this.tableSort()
    },
    tableSort() {
      this.tableVariable.sort(function (a, b) {
        return a.id - b.id
      })
      this.tableSelect.sort(function (a, b) {
        return a.id - b.id
      })
    },
    selectType() {
      console.log(this.addForm.type)
      if (this.addForm.type === 'CONSTANT') {
        this.hidden.lower_bound = true
        this.hidden.upper_bound = true
        this.hidden.length = false
        this.hidden.value = false
      } else if (this.addForm.type === 'ENUM') {
        this.hidden.lower_bound = true
        this.hidden.upper_bound = true
        this.hidden.length = false
        this.hidden.value = false
      } else if (this.addForm.type === 'INT8') {
        this.hidden.lower_bound = false
        this.hidden.upper_bound = false
        this.hidden.length = true
        this.hidden.value = true
      } else if (this.addForm.type === 'INT16') {
        this.hidden.lower_bound = false
        this.hidden.upper_bound = false
        this.hidden.length = true
        this.hidden.value = true
      } else if (this.addForm.type === 'INT32') {
        this.hidden.lower_bound = false
        this.hidden.upper_bound = false
        this.hidden.length = true
        this.hidden.value = true
      } else if (this.addForm.type === 'FLOAT') {
        this.hidden.lower_bound = false
        this.hidden.upper_bound = false
        this.hidden.length = false
        this.hidden.value = true
      } else {
        this.hidden.lower_bound = true
        this.hidden.upper_bound = true
        this.hidden.length = true
        this.hidden.value = true
      }
    },
    getProtocol() {
      this.$http
        .post(this.Global_Api + '/api/generation/protocol_list', this.itemInfo)
        .then((response) => {
          console.log(response.data.protocol_list)
          let temp_data = response.data.protocol_list
          for (let i = 0; i < temp_data.length; i++) {
            let temp_dict = { value: temp_data[i]['subject_name'], label: temp_data[i]['subject_name'] }
            this.optionsProtocol.push(temp_dict)
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    getCurrentProtocol() {
      this.$http
        .post(this.Global_Api + '/api/generation/current_protocol', { protocol: this.frame, item_id: this.itemInfo.id })
        .then((response) => {
          console.log(response.data)
          this.rawVaruableData = response.data.result
          this.tableVariable = this.rawData
          this.tableSelect = this.rawVaruableData
          this.deleteLeftFromRight()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    deleteLeftFromRight() {
      console.log(this.tableVariable)
      console.log(this.tableSelect)
      let temp = []
      for (let i = 0; i < this.tableVariable.length; i++) {
        let j = 0
        for (; j < this.tableSelect.length; j++) {
          if (this.tableVariable[i]['id'] === this.tableSelect[j]['id']) break
        }
        if (j === this.tableSelect.length) {
          temp.push(this.tableVariable[i])
        }
      }
      this.tableVariable = temp
    },
  },
  created() {
    this.getItemInfo()
    this.pageList()
    this.getProtocol()
    // this.getCurrentProtocol()
  },
  mounted() {},
  watch: {
    tableSelect(val) {
      // console.log(val)
      this.disabled.commit = val.length === 0
    },
    tableVariable(val) {
      console.log(val)
    },
  },
}
</script>

<style scoped></style>
