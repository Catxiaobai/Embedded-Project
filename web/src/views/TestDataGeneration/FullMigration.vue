<template>
  <div id="fullState">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="15">
          <div class="grid-content">
            <div id="action" style="display: flex; margin-bottom: 20px">
              <div id="stateAction" style="margin-left: 35%">
                <el-button type="primary" @click="fullMigration">全迁移覆盖</el-button>
              </div>
            </div>
            <div
              id="myDiagramDiv"
              v-show="diagram.state"
              style="background-color: whitesmoke; border: solid 1px black; width: 100%; height: 550px"
              ref="generatePicture"
            ></div>
          </div>
        </el-col>
        <el-col :span="9">
          <div class="grid-content">
            <div>
              <a style="font-size: 30px; margin-left: 30%">测试用例集</a>
              <el-card style="margin-top: 30px; height: 550px">
                <div style="overflow: auto; height: 500px">
                  <p v-for="(item, index) in test_cases_result" :key="index" style="margin-bottom: 20px">{{ item }}</p>
                </div>
              </el-card>
            </div>
          </div></el-col
        >
      </el-row>
    </el-card>
  </div>
</template>

<script>
import go from 'gojs'
import html2canvas from 'html2canvas'
const MAKE = go.GraphObject.make
export default {
  name: 'FullState.veu',
  inject: ['reload'],
  data() {
    return {
      doUpload: this.Global_Api + '/api/upload_umlfile',
      modelData: {
        nodeKeyProperty: 'text',
        nodeDataArray: [],
        linkDataArray: [],
      },
      nodeDataArray: [],
      linkDataArray: [],
      test_cases_result: '',
      buttonShow: {
        modeling: false,
        reduction: false,
        import: false,
        help: false,
      },
      uml: {
        path: '',
        name: '',
      },
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: [],
      },
      msg: 'result',
      test: 'tets',
      options: [
        {
          value: '外部交联环境',
          label: '外部交联环境',
          disabled: true,
        },
        {
          value: '功能处理',
          label: '功能处理',
          disabled: true,
        },
        {
          value: '功能层次',
          label: '功能层次',
          disabled: true,
        },
        {
          value: '状态迁移',
          label: '状态迁移',
        },
      ],
      value: '',
      itemInfo: '',
      diagram: {
        state: true,
        activity: false,
        timing: false,
        useCase: false,
        class: false,
        uml: false,
      },
      extrafile: '',
      umlSrc: '',
      umlSrcList: [],
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    fullMigration() {
      this.$http
        .post(this.Global_Api + '/api/generation/full_migration', { item: this.itemInfo })
        .then((response) => {
          console.log(response.data)
          this.test_cases_result = response.data.results
        })
        .catch(function (error) {
          console.log(error)
        })
    },
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
      this.modelingFromDatabase()
    },
    load() {
      this.myDiagram.model = go.Model.fromJson(this.modelData)
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
}
</script>

<style lang="scss" scoped>
.divHelp {
  margin-left: 55%;
  height: 40px;
  margin-top: -40px;
  z-index: 1;
  position: absolute;
}
</style>
