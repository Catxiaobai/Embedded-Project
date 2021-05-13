<template>
  <div>
    <el-card>
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="180"> </el-table-column>
        <el-table-column prop="name" label="指令" width="180"> </el-table-column>
        <el-table-column prop="script" label="脚本"> </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ScriptDatabase',
  data() {
    return {
      tableData: [
        {
          id: '1',
          name: 'Read',
          script: 'array=CH232.read(1)',
        },
        {
          id: '2',
          name: 'Write',
          script: 'array=CH232.write(22)',
        },
      ],
    }
  },
}
</script>

<style scoped></style>
