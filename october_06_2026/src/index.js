const { ApolloServer } = require('apollo-server');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

const server = new ApolloServer({ typeDefs, resolvers });

const PORT = process.env.PORT || 4000;
server.listen(PORT).then(({ url }) => {
  console.log(`Distributed systems GraphQL server: ${url}`);
});