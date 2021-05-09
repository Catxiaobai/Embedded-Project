<template>
  <div id="dataShow">
    <el-card>
      <el-table :data="tableData" border width="100%">
        <el-table-column v-for="(item, index) in desCol" :prop="item.prop" :label="item.label" :key="index"> </el-table-column>
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
  name: 'DataShow.vue',
  data() {
    return {
      tableData: [],
      desCol: [
        { prop: 'date', label: '日期' },
        { prop: 'name', label: '姓名' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
        { prop: 'address', label: '地址' },
      ],
    }
  },
}
</script>

<style scoped></style>
<style lang="scss"></style>
