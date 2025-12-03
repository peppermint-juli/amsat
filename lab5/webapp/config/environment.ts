// Map env variables and set defaults using the || operator in case no env variable is found

let loginPortalUrl = 'https://kubetest.sciserver.org/julianas-sciserver/login-portal/';
let graphqlUrl = 'https://kubetest.sciserver.org/julianas-sciserver/graphql';
let baseUrl = 'http://localhost:3000';

// if (process.env.ADYTON_ENV === 'prod') {
// baseUrl = 'http://kubetest.sciserver.org';
//   graphqlHttp = 'https://kubetest.sciserver.org/julianas-sciserver/graphql';
// }

export const env = {
  GRAPHQL_BASE_URL: graphqlUrl,
  BASE_URL: baseUrl,
  LOGIN_PORTAL_URL: loginPortalUrl
}
