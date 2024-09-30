const $ = go.GraphObject.make; // for conciseness in defining templates

let myDiagram = new go.Diagram(
  'myDiagramDiv', // must name or refer to the DIV HTML element
  {
    allowDelete: false,
    allowCopy: false,
    layout: $(go.ForceDirectedLayout, { isInitial: false }),
    'undoManager.isEnabled': true,
    // use "Modern" themes from extensions/Themes
    'themeManager.themeMap': new go.Map([
      { key: 'light', value: Modern },
      { key: 'dark', value: ModernDark },
    ]),
    'themeManager.changesDivBackground': true,
    'themeManager.currentTheme': document.getElementById('theme').value,
  }
);

myDiagram.themeManager.set('light', {
  colors: {
    primary: '#f7f9fc',
    green: '#62bd8e',
    blue: '#3999bf',
    purple: '#7f36b0',
    red: '#c41000',
  },
});
myDiagram.themeManager.set('dark', {
  colors: {
    primary: '#4a4a4a',
    green: '#429e6f',
    blue: '#3f9fc6',
    purple: '#9951c9',
    red: '#ff4d3d',
  },
});

// the template for each attribute in a node's array of item data
const itemTempl = $(go.Panel,
  'Horizontal',
  { margin: new go.Margin(2, 0) },
  $(go.Shape,
    { desiredSize: new go.Size(15, 15), strokeWidth: 0, margin: new go.Margin(0, 5, 0, 0) },
    new go.Binding('figure', 'figure'),
    new go.ThemeBinding('fill', 'color').ofData()
  ),
  $(go.TextBlock,
    { font: '14px sans-serif', stroke: 'black' },
    new go.Binding('text', 'name'),
    new go.Binding('font', 'iskey', (k) => (k ? 'italic 14px sans-serif' : '14px sans-serif')),
    new go.ThemeBinding('stroke', 'text')
  )
);

// define the Node template, representing an entity
myDiagram.nodeTemplate = $(go.Node,
  'Auto', // the whole node panel
  {
    selectionAdorned: true,
    resizable: true,
    layoutConditions: go.LayoutConditions.Standard & ~go.LayoutConditions.NodeSized,
    fromSpot: go.Spot.LeftRightSides,
    toSpot: go.Spot.LeftRightSides,
  },
  new go.Binding('location', 'location').makeTwoWay(),
  // whenever the PanelExpanderButton changes the visible property of the "LIST" panel,
  // clear out any desiredSize set by the ResizingTool.
  new go.Binding('desiredSize', 'visible', (v) => new go.Size(NaN, NaN)).ofObject('LIST'),
  // define the node's outer shape, which will surround the Table
  $(go.Shape, 'RoundedRectangle', { stroke: '#e8f1ff', strokeWidth: 3 }, new go.ThemeBinding('fill', 'primary')),
  $(go.Panel,
    'Table',
    { margin: 8, stretch: go.Stretch.Fill },
    $(go.RowColumnDefinition, { row: 0, sizing: go.Sizing.None }),
    // the table header
    $(go.TextBlock,
      {
        row: 0,
        alignment: go.Spot.Center,
        margin: new go.Margin(0, 24, 0, 2), // leave room for Button
        font: 'bold 18px sans-serif',
      },
      new go.Binding('text', 'key'),
      new go.ThemeBinding('stroke', 'text')
    ),
    // the collapse/expand button
    $('PanelExpanderButton',
      'LIST', // the name of the element whose visibility this button toggles
      { row: 0, alignment: go.Spot.TopRight },
      new go.ThemeBinding('ButtonIcon.stroke', 'text')
    ),
    $(go.Panel,
      'Table',
      { name: 'LIST', row: 1, alignment: go.Spot.TopLeft },
      $(go.TextBlock,
        'Attributes',
        {
          row: 0,
          alignment: go.Spot.Left,
          margin: new go.Margin(3, 24, 3, 2),
          font: 'bold 15px sans-serif',
        },
        new go.ThemeBinding('stroke', 'text')
      ),
      $('PanelExpanderButton', 'NonInherited', { row: 0, alignment: go.Spot.Right }, new go.ThemeBinding('ButtonIcon.stroke', 'text')),
      $(go.Panel,
        'Vertical',
        {
          row: 1,
          name: 'NonInherited',
          alignment: go.Spot.TopLeft,
          defaultAlignment: go.Spot.Left,
          itemTemplate: itemTempl,
        },
        new go.Binding('itemArray', 'items')
      ),
      $(go.TextBlock,
        'Inherited Attributes',
        {
          row: 2,
          alignment: go.Spot.Left,
          margin: new go.Margin(3, 24, 3, 2), // leave room for Button
          font: 'bold 15px sans-serif',
        },
        new go.Binding('visible', 'inheritedItems', (arr) => Array.isArray(arr) && arr.length > 0),
        new go.ThemeBinding('stroke', 'text')
      ),
      $('PanelExpanderButton',
        'Inherited',
        { row: 2, alignment: go.Spot.Right },
        new go.Binding('visible', 'inheritedItems', (arr) => Array.isArray(arr) && arr.length > 0),
        new go.ThemeBinding('ButtonIcon.stroke', 'text')
      ),
      $(go.Panel,
        'Vertical',
        {
          row: 3,
          name: 'Inherited',
          alignment: go.Spot.TopLeft,
          defaultAlignment: go.Spot.Left,
          itemTemplate: itemTempl,
        },
        new go.Binding('itemArray', 'inheritedItems')
      )
    )
  ) // end Table Panel
); // end Node

// define the Link template, representing a relationship
myDiagram.linkTemplate = $(go.Link, // the whole link panel
  {
    selectionAdorned: true,
    layerName: 'Background',
    reshapable: true,
    routing: go.Routing.AvoidsNodes,
    corner: 5,
    curve: go.Curve.JumpOver,
  },
  $(go.Shape, // the link shape
    { stroke: '#f7f9fc', strokeWidth: 3 },
    new go.ThemeBinding('stroke', 'link')
  ),
  $(go.TextBlock, // the "from" label
    {
      textAlign: 'center',
      font: 'bold 14px sans-serif',
      stroke: 'black',
      segmentIndex: 0,
      segmentOffset: new go.Point(NaN, NaN),
      segmentOrientation: go.Orientation.Upright,
    },
    new go.Binding('text', 'text'),
    new go.ThemeBinding('stroke', 'text')
  ),
  $(go.TextBlock, // the "to" label
    {
      textAlign: 'center',
      font: 'bold 14px sans-serif',
      stroke: 'black',
      segmentIndex: -1,
      segmentOffset: new go.Point(NaN, NaN),
      segmentOrientation: go.Orientation.Upright,
    },
    new go.Binding('text', 'toText'),
    new go.ThemeBinding('stroke', 'text')
  )
);


export function init(data) {

    data = JSON.parse(data)
    // Since 2.2 you can also author concise templates with method chaining instead of GraphObject.make
    // For details, see https://gojs.net/latest/intro/buildingObjects.html

    let nodeDataArray = [];
    let x = 0, y = 0;

    // Centro del canvas
    const centerX = 400;
    const centerY = 400;

    // Número de vértices
    const vertices = data.entities.length;

    // Distancia del centro a cada entidad
    const radius = 60 * vertices;

    // Función para dibujar el polígono
    function createVertices(centerX, centerY, radius, vertices) {
      let points = []
      for (let i = 0; i < vertices; i++) {
          const angle = (i * 2 * Math.PI) / vertices;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);
          points.push([x,y])
      }
      return points;
    }

    let points = createVertices(centerX, centerY, radius, vertices);
    let count = 0;

    for (const ent of data.entities) {
      let x = points[count][0], y = points[count][1]
      let attrs = [];
      for (const attr of ent.attributes) {
        attrs.push(
          { name: attr.name, iskey: true, figure: 'Decision', color: 'purple' }
        )
      }

      nodeDataArray.push(
        {
          key: ent.name,
          location: new go.Point(x, y),
          items: attrs
        }
      );

      count++;
    }
  
    let linkDataArray = [];
    for (const rel of data.relations) {
      linkDataArray.push(
        { from: rel.source, to: rel.target, text: '0..N', toText: '1' }
      )
    }

    /*
    const nodeDataArray = [
      {
        key: 'Products',
        location: new go.Point(250, 250),
        items: [
          { name: 'ProductID', iskey: true, figure: 'Decision', color: 'purple' },
          { name: 'ProductName', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'ItemDescription', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'WholesalePrice', iskey: false, figure: 'Circle', color: 'green' },
          { name: 'ProductPhoto', iskey: false, figure: 'TriangleUp', color: 'red' },
        ],
        inheritedItems: [
          { name: 'SupplierID', iskey: false, figure: 'Decision', color: 'purple' },
          { name: 'CategoryID', iskey: false, figure: 'Decision', color: 'purple' },
        ],
      },
      {
        key: 'Suppliers',
        location: new go.Point(500, 0),
        items: [
          { name: 'SupplierID', iskey: true, figure: 'Decision', color: 'purple' },
          { name: 'CompanyName', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'ContactName', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'Address', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'ShippingDistance', iskey: false, figure: 'Circle', color: 'green' },
          { name: 'Logo', iskey: false, figure: 'TriangleUp', color: 'red' },
        ],
        inheritedItems: [],
      },
      {
        key: 'Categories',
        location: new go.Point(0, 30),
        items: [
          { name: 'CategoryID', iskey: true, figure: 'Decision', color: 'purple' },
          { name: 'CategoryName', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'Description', iskey: false, figure: 'Hexagon', color: 'blue' },
          { name: 'Icon', iskey: false, figure: 'TriangleUp', color: 'red' },
        ],
        inheritedItems: [{ name: 'SupplierID', iskey: false, figure: 'Decision', color: 'purple' }],
      },
      {
        key: 'Order Details',
        location: new go.Point(600, 350),
        items: [
          { name: 'OrderID', iskey: true, figure: 'Decision', color: 'purple' },
          { name: 'UnitPrice', iskey: false, figure: 'Circle', color: 'green' },
          { name: 'Quantity', iskey: false, figure: 'Circle', color: 'green' },
          { name: 'Discount', iskey: false, figure: 'Circle', color: 'green' },
        ],
        inheritedItems: [{ name: 'ProductID', iskey: false, figure: 'Decision', color: 'purple' }],
      },
    ];
    
    
    const linkDataArray = [
      { from: 'Products', to: 'Suppliers', text: '0..N', toText: '1' },
      { from: 'Products', to: 'Categories', text: '0..N', toText: '1' },
      { from: 'Order Details', to: 'Products', text: '0..N', toText: '1' },
      { from: 'Categories', to: 'Suppliers', text: '0..N', toText: '1' },
    ];*/
    myDiagram.model = new go.GraphLinksModel({
      copiesArrays: true,
      copiesArrayObjects: true,
      nodeDataArray: nodeDataArray,
      linkDataArray: linkDataArray,
    });
  }

  export const changeTheme = () => {
    const myDiagram = go.Diagram.fromDiv('myDiagramDiv');
    if (myDiagram) {
      myDiagram.themeManager.currentTheme = document.getElementById('theme').value;
    }
  };