require 'rubygems'
require 'ruby-graphviz'

g = GraphViz.new(:g, :type => :digraph)

feature_nodes = []

layers = [40, 20, 10, 1]
previous_nodes = feature_nodes

layers.each_with_index do |layer, layer_index|
  next_nodes = []
  0.upto(layer - 1) do |i|
    new_node = g.add_nodes("L_#{layer_index}_#{i}")
    next_nodes << new_node
    previous_nodes.each do |previous_node|
      g.add_edges(previous_node, new_node)
    end
  end
  previous_nodes = next_nodes
end

g.output(png: 'fann.png')
