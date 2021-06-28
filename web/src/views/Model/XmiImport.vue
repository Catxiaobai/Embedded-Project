<template>
  <div id="XMI">
    <el-card>
      <div id="action" style="display: flex; margin-bottom: 20px">
        <el-upload :action="doUpload" :on-success="handleImport" :show-file-list="false">
          <a style="color: #38b2ff; margin-left: 500px"> XMI文件导入</a>
        </el-upload>
        <el-button type="primary" style="margin-left: 30%; margin-top: -10px" @click="save">save</el-button>
      </div>
      <div id="myDiagramDiv" style="background-color: whitesmoke; border: solid 1px black; width: 100%; height: 560px" ref="generatePicture"></div>
    </el-card>
    <div id="addNode">
      <el-dialog :close-on-click-modal="false" title="ADD" :visible.sync="visible.addNodeDialog" center width="55%">
        <el-form :model="addNodeForm" :rules="rules" ref="addNodeForm" style="display: flex">
          <el-card id="nodeCard">
            newState
            <el-form-item label="State name" label-width="120px" prop="node_name">
              <el-input v-model="addNodeForm.node_name" clearable placeholder="please enter state name"></el-input>
            </el-form-item>
            <el-form-item label="State label" label-width="120px" prop="node_label">
              <el-input v-model="addNodeForm.node_label" clearable placeholder="please enter state label"></el-input>
            </el-form-item>
          </el-card>
          <el-card id="linkCard" style="margin-left: 10px">
            link
            <el-form-item label="link_name" label-width="120px" prop="link_name">
              <el-input v-model="addNodeForm.link_name" clearable placeholder="please enter link name"></el-input>
            </el-form-item>
            <el-form-item label="source" label-width="120px" prop="source">
              <el-input v-model="addNodeForm.source" clearable placeholder="please enter source" disabled></el-input>
            </el-form-item>
            <el-form-item label="target" label-width="120px" prop="target">
              <el-input v-model="addNodeForm.target" clearable placeholder="please enter target"></el-input>
            </el-form-item>
            <el-form-item label="action" label-width="120px" prop="action">
              <el-input v-model="addNodeForm.action" clearable placeholder="please enter action"></el-input>
            </el-form-item>
            <el-form-item label="event" label-width="120px" prop="event">
              <el-input v-model="addNodeForm.event" clearable placeholder="please enter event"></el-input>
            </el-form-item>
            <el-form-item label="condition" label-width="120px" prop="condition">
              <el-input v-model="addNodeForm.condition" clearable placeholder="please enter condition"></el-input>
            </el-form-item>
          </el-card>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.addNodeDialog = false">No</el-button>
          <el-button type="primary" @click="handleAddNodeCommit('addNodeForm')">Yes</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="addLink">
      <el-dialog :close-on-click-modal="false" title="添加边" :visible.sync="visible.addLinkDialog" center width="30%" :show-close="false">
        <el-form :model="addLinkForm" :rules="rules" ref="addLinkForm" style="display: flex">
          <el-card style="margin-left: 10px">
            <el-form-item label="link_name" label-width="120px" prop="link_name">
              <el-input v-model="addLinkForm.link_name" clearable placeholder="请输入边的name"></el-input>
            </el-form-item>
            <el-form-item label="source" label-width="120px" prop="source">
              <el-input v-model="addLinkForm.source" clearable placeholder="请输入source" disabled></el-input>
            </el-form-item>
            <el-form-item label="target" label-width="120px" prop="target">
              <el-input v-model="addLinkForm.target" clearable placeholder="请输入target" disabled></el-input>
            </el-form-item>
            <el-form-item label="action" label-width="120px" prop="action">
              <el-input v-model="addLinkForm.action" clearable placeholder="请输入action"></el-input>
            </el-form-item>
            <el-form-item label="event" label-width="120px" prop="event">
              <el-input v-model="addLinkForm.event" clearable placeholder="请输入event"></el-input>
            </el-form-item>
            <el-form-item label="condition" label-width="120px" prop="condition">
              <el-input v-model="addLinkForm.condition" clearable placeholder="请输入condition"></el-input>
            </el-form-item>
          </el-card>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="handleAddLinkCancel">取 消</el-button>
          <el-button type="primary" @click="handleAddLinkCommit('addLinkForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import go from 'gojs'

export default {
  data() {
    return {
      doUpload: this.Global_Api + '/api/upload_file',
      itemInfo: '',
      modelData: {
        nodeKeyProperty: 'text',
        nodeDataArray: [],
        linkDataArray: [],
      },
      addNodeForm: {},
      addLinkForm: {},
      visible: {
        addNodeDialog: false,
        addLinkDialog: false,
      },
      rules: {
        node_name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        node_label: [{ required: true, message: '不能为空', trigger: 'blur' }],
        link_name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        source: [{ required: true, message: '不能为空', trigger: 'blur' }],
        target: [{ required: true, message: '不能为空', trigger: 'blur' }],
        action: [{ required: true, message: '不能为空', trigger: 'blur' }],
        event: [{ required: true, message: '不能为空', trigger: 'blur' }],
        condition: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
    }
  },
  methods: {
    init() {
      const $ = go.GraphObject.make
      const _this = this
      _this.myDiagram = $(go.Diagram, 'myDiagramDiv', {
        'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
        'undoManager.isEnabled': true,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 40,
          defaultElectricalCharge: 180,
          randomNumberGenerator: null,
          infinityDistance: 210,
        }),
      })
      // _this.myDiagram.toolManager.mouseMoveTools.insertAt(0, new LinkLabelDraggingTool())
      _this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        // 图标的style
        $(go.Shape, 'Circle', {
          desiredSize: new go.Size(67, 67),
          fill: $(go.Brush, 'Linear', { 0: 'rgb(201, 218, 248)', 1: 'rgb(201, 218, 248)' }),
          stroke: 'black',
          portId: '',
          fromLinkable: true,
          fromLinkableSelfNode: true,
          fromLinkableDuplicates: true,
          toLinkable: true,
          toLinkableSelfNode: true,
          toLinkableDuplicates: true,
          cursor: 'pointer',
        }),
        // 字体的style
        $(
          go.TextBlock,
          {
            font: 'bold 11pt helvetica, bold arial, sans-serif',
            editable: true, // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        ),
        // 悬浮框
        {
          cursor: 'pointer',
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'label'))), // end of Adornment
        }
      )
      _this.myDiagram.linkTemplate = $(
        go.Link, // the whole link panel
        {
          curve: go.Link.Bezier,
          adjusting: go.Link.Stretch,
          reshapable: true,
          relinkableFrom: true,
          relinkableTo: true,
        },
        {
          cursor: 'pointer',
          toolTip: $(
            'ToolTip',
            { 'Border.fill': 'whitesmoke', 'Border.stroke': 'black' },
            $(go.TextBlock, { margin: 4 }, new go.Binding('text', '', tooltipTextConverter))
          ),
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          { strokeWidth: 1.5 }
        ),
        $(
          go.Shape, // the arrowhead
          { toArrow: 'standard', stroke: null }
        ),
        $(
          go.Panel,
          'Auto',
          { cursor: 'move' }, // visual hint that the user can do something with this link label
          $(
            go.Shape, // the label background, which becomes transparent around the edges
            {
              fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
              stroke: null,
            }
          ),
          $(
            go.TextBlock,
            'transition', // the label text
            {
              textAlign: 'center',
              font: '10pt helvetica, arial, sans-serif',
              stroke: 'black',
              margin: 4,
              editable: false, // editing the text automatically updates the model data
            },
            new go.Binding('text', 'text').makeTwoWay()
          ),
          new go.Binding('segmentOffset', 'segmentOffset', go.Point.parse).makeTwoWay(go.Point.stringify)
        )
      )
      // 鼠标悬停提示窗
      function tooltipTextConverter(info) {
        let str = ''
        str += 'name: ' + info.text + '\n'
        str += 'source: ' + info.from + '\n'
        str += 'target: ' + info.to + '\n'
        str += 'event: ' + info.event + '\n'
        str += 'condition: ' + info.condition + '\n'
        str += 'action: ' + info.action + '\n'
        return str
      }
      _this.myDiagram.toolManager.hoverDelay = 10
      _this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
        go.Adornment,
        'Spot',
        $(
          go.Panel,
          'Auto',
          $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
          $(go.Placeholder) // this represents the selected Node
        ),
        // the button to create a "next" node, at the top-right corner
        $(
          'Button',
          {
            alignment: go.Spot.TopRight,
            // click: addNodeAndLink // this function is defined below
            click: _this.addNewNode,
          },
          $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
        ) // end button
      ) // end Adornment
      // 监听添加线事件
      _this.myDiagram.addDiagramListener('LinkDrawn', function (e) {
        _this.addNewLink(e)
      })
    },
    load() {
      this.myDiagram.model = go.Model.fromJson(this.modelData)
    },
    save() {
      console.log(this.myDiagram.model.toJson())
      this.$http.post(this.Global_Api + '/api/save_model_to_xmi_model', this.myDiagram.model.toJson()).then((response) => {
        if (response.data.error_code === 0) {
          console.log(response)
          this.$message.success('保存成功')
        } else {
          this.$message.error(response.data.error_message)
        }
      })
    },
    addNewNode(e, obj) {
      console.log(e, obj)
      let adorn = obj.part
      let fromData = adorn.adornedPart.data
      console.log(fromData)
      console.log(this.modelData)
      this.visible.addNodeDialog = true
      this.addNodeForm.source = fromData.text
    },
    addNewLink(e) {
      console.log(e.subject.data)
      this.visible.addLinkDialog = true
      this.addLinkForm.target = e.subject.data.to
      this.addLinkForm.source = e.subject.data.from
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleAddNodeCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$message.success('添加成功')
          this.visible.addNodeDialog = false
          console.log(this.addNodeForm)
          let new_node = { text: this.addNodeForm.node_name, label: this.addNodeForm.node_label }
          let new_link = {
            text: this.addNodeForm.link_name,
            from: this.addNodeForm.source,
            to: this.addNodeForm.target,
            event: this.addNodeForm.event,
            condition: this.addNodeForm.condition,
            action: this.addNodeForm.action,
          }
          this.myDiagram.model.addNodeData(new_node)
          this.myDiagram.model.addLinkData(new_link)
          this.$refs[formName].resetFields()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleAddLinkCommit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$message.success('添加成功')
          console.log(this.addLinkForm)
          let new_link = {
            text: this.addLinkForm.link_name,
            from: this.addLinkForm.source,
            to: this.addLinkForm.target,
            event: this.addLinkForm.event,
            condition: this.addLinkForm.condition,
            action: this.addLinkForm.action,
          }
          this.myDiagram.undoManager.undo()
          this.myDiagram.model.addLinkData(new_link)
          this.visible.addLinkDialog = false
          this.$refs[formName].resetFields()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleAddLinkCancel() {
      this.myDiagram.undoManager.undo()
      this.visible.addLinkDialog = false
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    handleImport(code, file) {
      this.$http.post(this.Global_Api + '/api/import_xmi', { name: file.name, item: this.itemInfo }).then((response) => {
        if (response.data.error_code === 0) {
          console.log(response)
          this.$message.success('导入成功')
          this.modelingFromDatabase()
        } else {
          this.$message.error(response.data.error_message)
        }
      })
    },
    modelingFromDatabase() {
      this.$http.post(this.Global_Api + '/api/modeling_from_db', this.itemInfo).then((response) => {
        if (response.data.error_code === 0) {
          console.log(response)
          this.modelData.nodeDataArray = response.data.nodeDataArray
          this.modelData.linkDataArray = response.data.linkDataArray
          this.load()
        } else {
          this.$message.error(response.data.error_message)
        }
      })
    },
  },
  created() {
    this.getItemInfo()
  },
  mounted() {
    this.init()
  },
}
</script>

<style lang="scss" scoped></style>
