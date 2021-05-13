<template>
  <div>
    <el-card>
      <el-table :data="tableData" style="width: 100%" border>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="ID:">
                <span style="font-weight: normal">{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="标识:">
                <span style="font-weight: normal">{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="类型:">
                <span style="font-weight: normal">{{ props.row.type }}</span>
              </el-form-item>
              <el-form-item label="原型:">
                <span style="font-weight: normal">{{ props.row.prototype }}</span>
              </el-form-item>
              <el-form-item label="参数:">
                <span style="font-weight: normal">{{ props.row.parameter }}</span>
              </el-form-item>
              <el-form-item label="返回值:">
                <span style="font-weight: normal">{{ props.row.return }}</span>
              </el-form-item>
              <el-form-item label="说明:">
                <span style="font-weight: normal">{{ props.row.explain }}</span>
              </el-form-item>
              <el-form-item label="应用场景:">
                <span style="font-weight: normal">{{ props.row.application }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="ID" width="40"> </el-table-column>
        <el-table-column prop="name" label="标识" width="120" align="center"> </el-table-column>
        <el-table-column prop="type" label="类型" width="180"> </el-table-column>
        <el-table-column prop="prototype" label="原型" width="180" style="white-space: pre-line"> </el-table-column>
        <el-table-column prop="function" label="功能"> </el-table-column>
        <!--        <el-table-column prop="parameter" label="参数"> </el-table-column>-->
        <!--        <el-table-column prop="return" label="返回值"> </el-table-column>-->
      </el-table>
      <!--      <div>-->
      <!--        <el-table :data="tableData" border style="width: 100%">-->
      <!--          <el-table-column prop="id" label="ID" width="40"> </el-table-column>-->
      <!--          <el-table-column prop="name" label="标识" width="100"> </el-table-column>-->
      <!--          <el-table-column prop="type" label="类型"> </el-table-column>-->
      <!--          <el-table-column prop="prototype" label="原型"> </el-table-column>-->
      <!--          <el-table-column prop="function" label="功能"> </el-table-column>-->
      <!--          <el-table-column prop="parameter" label="参数"> </el-table-column>-->
      <!--          <el-table-column prop="return" label="返回值"> </el-table-column>-->
      <!--          <el-table-column prop="explain" label="说明"> </el-table-column>-->
      <!--          <el-table-column prop="application" label="应用场景"> </el-table-column>-->
      <!--        </el-table>-->
      <!--      </div>-->
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
          name: 'ReadL',
          type: '通道读（按长度）',
          prototype: '通道.Read(length)',
          function: '从通道读取指定长度的数据内容（字节数组）',
          parameter: 'Length：指定需要读取的数据长度',
          return: '成功则返回指定长度的数据；失败则返回None',
          explain: '需要判断Read操作是否成功。当通道缓存中的数据大于等于指定读取长度时，读取成功；否则，读取失败。读取成功后，读取到的数据从缓存中取出。',
          application: '测试人员为了验证待测系统是否按照预期向外发送了预期长度的数据内容，需要使用硬件通道从待测系统读取length个字节的数据',
        },
        {
          id: '2',
          name: 'BlockReadL',
          type: '通道阻塞读(按长度)',
          prototype: '通道.BlockRead(length)',
          function: '从指定通道读取指定长度的字节数据，如果没有足够长度数据则一直等待。',
          parameter: 'Length：指定需要读取的数据长度',
          return: '通道里的数据长度大于等于length，则返回指定长度的数据；否则阻塞调用线程',
          explain: '不需要判断BlockRead的操作是否成功。读取到的数据从缓存中取出',
          application:
            '测试人员为了验证待测是系统是否按照预期向外发送了指定长度的数据，并且，确认收到了正确的数据，' +
            '后续的测试才有意义，否则，测试脚本应该一直等待，直到收到足够长度的数据为止。需要调用通道. BlockRead(length)',
        },
        {
          id: '3',
          name: 'ReadHT',
          type: '通道读(按头尾标记)',
          prototype: '通道.Read([head],[tail])',
          function: '使用指定的通道从待测系统读取符合头尾标记特征的数据',
          parameter:
            'head：开始标识，是一个字节序列。即读取到的数据的必须以[head]开始。\n' + 'tail：结束标识，是一个字节序列。即读取到的数据的必须以[tail]结束。\n',
          return: '成功则返回[head]XXXXXXXX[tail]；失败则返回None',
          explain: '需要判断Read操作是否成功。读取成功后，读取到的数据和[head]之前的数据从缓存中清除',
          application: '测试人员为了验证待测系统是否按照预期向外发送了一段用【head】和【tail】标志标记的数据。调用通道.Read([head],[tail])方法达到效果',
        },
        {
          id: '4',
          name: 'BlockReadHT',
          type: '通道阻塞读 (按头尾标记)',
          prototype: '通道.BlockRead([head],[tail])',
          function: '使用指定的通道从待测系统阻塞地读取符合头尾标记特征的数据',
          parameter:
            'head：开始标识，是一个字节序列。即读取到的数据的必须以[head]开始。\n' + 'Tail：结束标识，是一个字节序列。即读取到的数据的必须以[tail]结束。\n',
          return: '如果通道接受到的数据里存在符合要求的数据内容，则返回[head]XXXXXXXX[tail]',
          explain: '不需要判断BlockRead的操作是否成功。读取到的数据和[head]之前的数据从缓存中清除',
          application:
            '测试人员为了验证待测系统向外发送了一段用【head】和【tail】标志标记的数据，并且，在读到有效数据之前，执行后续的步骤没有意义，' +
            '必须等到读取到正确的数据以后才能继续。调用BlockRead([head],[tail])方法达到效果',
        },
        {
          id: '5',
          name: 'Write',
          type: '通道写',
          prototype: '通道.Write(buffer)',
          function: '使用指定通道向待测系统写入指定的数据',
          parameter: 'buffer：需要向待测系统写入的字节内容数组',
          return: '成功则返回 True；失败则返回 False',
          explain: '通道连接异常时（环境设置时提示通道打开失败），写入失败。需要对Write的返回结果进行判断，根据其结果做进一步的验证与测试',
          application: '测试人员为了向待测系统发送特定的操作指令，写入一段对应的字节数据，需要调用通道.Write (buffer)达到预期的效果',
        },
        {
          id: '6',
          name: 'Clear',
          type: '通道缓存清理',
          prototype: '通道.Clear(count=-1)',
          function: '清理通道缓存里的历史数据',
          parameter: 'Count：需要清理的bit数量，默认值-1，代表全部清除；大于0的值有效',
          return:
            '成功则返回清理操作过程中被丢弃的缓存内容；失败则返回None。\n' +
            '返回值.Value：表示清除成功或失败。\n' +
            '返回值.Data：被清理掉的数据。\n' +
            '返回值.Count：表示Clear掉的数据的个数，以bit为单位\n',
          explain: '清除缓存数据，保证下次Read的数据是清除之后的最新数据',
          application: '测试人员为了在测试某个功能之前，清理之前其他操作遗留下来的垃圾数据，否则，会影响到本次测试的内容，' + '可以调用通道.Clear()方法来实现',
        },
        {
          id: '7',
          name: 'Seek',
          type: '通道缓存定位',
          prototype: '通道.Seek(identy)',
          function: '将通道缓存的数据开始位置定位到指定的标识位置。之前的数据被丢弃',
          parameter: 'Identy：字节序列，需要定位到的标识',
          return:
            '成功则返回定位操作丢弃掉的缓存内容；失败则返回 None。\n' +
            '返回值.Value：是否查找到字节序列。\n' +
            '返回值.Count：丢弃数据位数。\n' +
            '返回值.Data：丢弃的数据。\n',
          explain: '移动数据指针，直到匹配标识的字节序列为止。前面的数据被丢弃，缓存中的数据从标识字节序列开始。如果没有匹配到，则返回None。',
          application:
            '测试人员为了在测试某个功能时，希望接收到特定标志开头（如0XAABB）的帧数据，但是，实际上可能存在之前操作遗留下来的无关的噪音数据，' +
            '则需要调用通道.Seek(identy)，将通道里的数据定位到符合该特征的位置。',
        },
        {
          id: '8',
          name: 'BlockSeek',
          type: '通道缓存阻塞定位',
          prototype: '通道.BlockSeek(identy)',
          function: '将通道缓存的数据开始位置以阻塞的方式定位到指定的标记位置',
          parameter: 'Identy：字节序列，需要定位到的标识',
          return:
            '如果通道里存在指定特征的数据，则返回定位操作丢弃掉的缓存内容；否则阻塞调用线程。\n' +
            '返回值.Value：是否查找到字节序列。\n' +
            '返回值.Count：丢弃数据位数。\n' +
            '返回值.Data：丢弃的数据。\n',
          explain: '移动数据指针，直到匹配参数为止。如果收到的数据都无法匹配，则阻塞进程，等待数据，直到收到能够匹配的数据再返回。',
          application:
            '测试人员为了在测试某个功能时，必须确保后面步骤读到的数据满足特定的特征开头，否则导致测试逻辑错误，但是，实际上可能存在其他的噪音数据，' +
            '则需要调用通道. BlockSeek(identy)，将通道里的数据定位到符合该特征的位置。',
        },
        {
          id: '9',
          name: 'Host',
          type: '通道Host',
          prototype: 'ip=通道.HostIP; ' + '\n' + 'port=通道.HostPort',
          function: '获取通道所属的客户端的IP地址和端口',
          parameter: '',
          return: '通道设备所属的客户端的地址和端口',
          explain: '通道所属的客户端，在项目的PC规划时设置。一般是在向该客户端发送实时任务时使用',
          application: '测试人员在测试某个功能时，希望查询某个通道所在的宿主计算机（客户端）的地址和端口信息',
        },
        {
          id: '10',
          name: 'Getter',
          type: '协议段Getter',
          prototype: 'v=协议.协议段.Value',
          function: '读取指定协议段的当前值',
          parameter: '',
          return: '测试脚本环境里指定协议段的当前值',
          explain: '',
          application:
            '在使用协议对象进行一次Read或者BlockBlock的操作之后，根据当前某个特定协议段当前的值，对下一步的测试与验证的步骤进行决策，' +
            '需要使用协议段的Getter，得到想要的实际值',
        },
        {
          id: '11',
          name: 'Setter',
          type: '协议段Setter',
          prototype: '协议.协议段.Value=v',
          function: '为某个协议段进行赋值',
          parameter: '',
          return: '无',
          explain: '',
          application: '在使用协议对象向待测系统发送指令之前，设置好各个协议段的当前值，需用协议段Setter达到效果',
        },
        {
          id: '12',
          name: 'PRead',
          type: '协议读',
          prototype: '协议.Read()',
          function: '使用指定的协议从待测系统读取一帧内容',
          parameter: '',
          return: '成功则返回True；失败则返回False',
          explain: '',
          application: '为了验证待测系统是否向外发送了指定DPD协议所规定的内容，需用调用协议.Read()后检查其返回值和协议段的内容是否满足预期',
        },
        {
          id: '13',
          name: 'PBlockRead',
          type: '协议阻塞读',
          prototype: '协议.BlockRead()',
          function: '使用指定的协议从待测系统阻塞读取一帧内容，直到读取到数据为止',
          parameter: '',
          return: '如果成功读到数据则返回；否则阻塞调用线程',
          explain: '',
          application: '以阻塞方式读取一帧数据，只有成功读取到数据内容以后，后续的测试步骤才能继续执行，需要调用协议.BlockRead()达到目的效果',
        },
        {
          id: '14',
          name: 'FromBytes',
          type: '协议解码',
          prototype: '协议.FromBytes(buffer)',
          function: '为某个协议段进行赋值',
          parameter: 'buffer：需要解析到协议上的字节数组',
          return: '成功则返回 True；失败则返回 False',
          explain: '',
          application: '将一组无格式的字节数组翻译成应用层协议（DPD），以便查看其各个协议段代表的真实物理意义，需要调用协议.FromBytes(buffer)',
        },
        {
          id: '15',
          name: 'PWrite',
          type: '协议写',
          prototype: '协议.Write()',
          function: '使用指定的协议向待测系统写入一帧内容',
          parameter: '',
          return: '成功则返回 True；失败则返回 False',
          explain: '',
          application: '为了向待测系统写入一帧指定DPD协议，需要调用协议.Write()',
        },
        {
          id: '16',
          name: 'PToBytes',
          type: '协议编码',
          prototype: '协议.ToBytes()',
          function: '使用指定的协议根据其字段值编码到一个字节数组',
          parameter: '',
          return: '返回协议定义长度的字节数组',
          explain: '',
          application:
            '为了将一组应用协议（DPD）描述的内容编码为字节数组进行处理（加密，压缩等）以后，再向待测系统发送出去，' +
            '需要调用协议.ToBytes()得到字节数组，然后经过处理以后，调用通道.Write(buffer)发送出去',
        },
      ],
    }
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
