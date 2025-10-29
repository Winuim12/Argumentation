// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  if (!CY_NODES || !CY_EDGES) return;

  // if no nodes, skip
  if (CY_NODES.length === 0 && CY_EDGES.length === 0) return;

  const cy = cytoscape({
    container: document.getElementById('cy'),
    elements: {
      nodes: CY_NODES.map(n => ({ data: n.data })),
      edges: CY_EDGES.map(e => ({ data: e.data }))
    },
    style: [
      {
        selector: 'node',
        style: {
          'label': 'data(label)',
          'text-valign': 'center',
          'text-halign': 'center',
          'background-color': '#1976d2',
          'color': '#fff',
          'text-outline-width': 2,
          'text-outline-color': '#1976d2',
          'width': '50px',
          'height': '50px'
        }
      },
      {
        selector: 'edge',
        style: {
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'width': 3,
          'line-color': '#555',
          'target-arrow-color': '#555'
        }
      }
    ],
    layout: { name: 'cose', animate: true }
  });

  // add click handler: highlight in/out edges
  cy.on('tap', 'node', function (evt) {
    const node = evt.target;
    cy.elements().removeClass('faded');
    cy.elements().addClass('faded'); // fade all
    const connected = node.closedNeighborhood(); // node + neighbors + edges
    connected.removeClass('faded');
  });

  // style for faded
  cy.style()
    .selector('.faded')
    .style({ 'opacity': 0.15 })
    .update();
});
