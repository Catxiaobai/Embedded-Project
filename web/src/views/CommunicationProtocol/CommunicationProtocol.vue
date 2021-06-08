<template>
  <div id="mainDiv">
    <el-card style="height: 645px">
      <div id="formDiv" style="margin-top: 30px">
        <el-form :model="form" :rules="rules" ref="form" label-width="100px">
          <el-row>
            <el-col :span="8">
              <el-form-item label="主题名称" prop="subject_name">
                <el-input v-model="form.subject_name" placeholder="请填写主题名称"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="总线类型" prop="bus_type">
                <el-input v-model="form.bus_type" placeholder="请填写总线类型"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="日期" prop="date">
                <el-input v-model="form.date" placeholder="请填写日期"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="通讯方式" prop="communication_method">
                <el-input v-model="form.communication_method" placeholder="请填写通讯方式"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="刷新周期" prop="refresh_cycle">
                <el-input v-model="form.refresh_cycle" placeholder="请填写刷新周期"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="版本" prop="version">
                <el-input v-model="form.version" placeholder="请填写版本"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="帧头" prop="frame_header">
                <el-input v-model="form.frame_header" placeholder="请填写帧头"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="帧尾" prop="frame_tail">
                <el-input v-model="form.frame_tail" placeholder="请填写帧尾"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="校验方式" prop="check_method">
                <el-input v-model="form.check_method" placeholder="请填写校验方式"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      <div id="handleDiv" style="margin-left: 35%; margin-top: 20px">
        <el-button type="primary" @click="submitForm('form')">立即创建</el-button>
        <el-button @click="resetForm('form')" style="margin-left: 30px">重置</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'CommunicationProtocol',
  data() {
    return {
      form: {
        subject_name: '',
        date: '',
        version: '',
        bus_type: '',
        communication_method: '',
        refresh_cycle: '',
        frame_header: '',
        frame_tail: '',
        check_method: '',
        item_id: '',
      },
      rules: {
        subject_name: [{ required: true, message: '请填写主题名称', trigger: 'blur' }],
        date: [{ required: true, message: '请填写日期', trigger: 'blur' }],
        version: [{ required: true, message: '请填写版本', trigger: 'blur' }],
        bus_type: [{ required: true, message: '请填写总线类型', trigger: 'blur' }],
        communication_method: [{ required: true, message: '请填写通讯方式', trigger: 'blur' }],
        refresh_cycle: [{ required: true, message: '请填写刷新周期', trigger: 'blur' }],
        frame_header: [{ required: true, message: '请填写帧头', trigger: 'blur' }],
        frame_tail: [{ required: true, message: '请填写帧尾', trigger: 'blur' }],
        check_method: [{ required: true, message: '请填写校验方式', trigger: 'blur' }],
      },
      itemInfo: '',
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http
            .post(this.Global_Api + '/api/generation/add_protocol', this.form)
            .then((response) => {
              if (response.data.error_code === 0) {
                this.$message.success('添加成功')
                this.resetForm('form')
              } else {
                this.$message.error(response.data.error_message)
                console.log(response.data)
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          // alert('submit!')
          // console.log(this.form)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
  },
  created() {
    this.getItemInfo()
    this.form.item_id = this.itemInfo.id
  },
}
</script>

<style scoped></style>
