import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.CookieStore;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.protocol.ClientContext;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HTTP;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;

import com.google.gson.Gson;

public class Uploader {

	// private final String HOST = "localhost:5000";
	// private final String HOST = "10.1.22.41";
	private final String HOST = "204.236.169.123";
	private HttpClient httpclient;
	private CookieStore cookieStore;
	private HttpContext localContext;
	private Gson gson;

	public Uploader() {
		// initialize apache objects
		httpclient = new DefaultHttpClient();
		cookieStore = new BasicCookieStore();
		// Create local HTTP context
		localContext = new BasicHttpContext();
		// Bind custom cookie store to the local context
		localContext.setAttribute(ClientContext.COOKIE_STORE, cookieStore);
		// initialize Gson object
		gson = new Gson();
	}

	public boolean login(String email, String password) {
		try {
			boolean result = false;
			// login request
			String url = "http://" + HOST + "/login/";
			HttpPost request = new HttpPost(url);
			List<NameValuePair> nvpairs = new ArrayList<NameValuePair>();
			// nvpairs.add(new BasicNameValuePair("email", "bob@example.com"));
			// nvpairs.add(new BasicNameValuePair("password", "pass"));
			nvpairs.add(new BasicNameValuePair("email", email));
			nvpairs.add(new BasicNameValuePair("password", password));
			request.setEntity(new UrlEncodedFormEntity(nvpairs, HTTP.UTF_8));
			HttpResponse response = httpclient.execute(request, localContext);
			String redirectCode = "302 FOUND";
			if (response.getStatusLine().toString().contains(redirectCode)) {
				result = true;
			}
			HttpEntity entity = response.getEntity();
			EntityUtils.consume(entity);
			return result;
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			return false;
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			return false;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			return false;
		}
	}

	public int[] getAllScenarios() {
		try {
			int[] scenarioIDs = null;
			// overview request
			String url = "http://" + HOST + "/get_all_scenarios/";
			HttpGet request = new HttpGet(url);
			// Create a response handler
			ResponseHandler<String> handler = new BasicResponseHandler();
			// Pass handler and local context as parameters
			String responseBody = httpclient.execute(request, handler,
					localContext);
			scenarioIDs = gson.fromJson(responseBody, int[].class);
			return scenarioIDs;
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}

	public String getScenarioQuery(int scenarioID) {
		try {
			String scenarioQuery = "";
			// overview request
			String url = "http://" + HOST + "/get_scenario_query/" + scenarioID
					+ "/";
			HttpGet request = new HttpGet(url);
			// Create a response handler
			ResponseHandler<String> handler = new BasicResponseHandler();
			// Pass handler and local context as parameters
			String responseBody = httpclient.execute(request, handler,
					localContext);
			scenarioQuery = gson.fromJson(responseBody, String.class);
			return scenarioQuery;
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}

	public void sendQueryResultStructure(int scenarioID,
			String queryResultStructure) {
		try {
			// login request
			String url = "http://" + HOST + "/upload_query_result_structure/"
					+ scenarioID + "/";
			HttpPost request = new HttpPost(url);
			List<NameValuePair> nvpairs = new ArrayList<NameValuePair>();
			nvpairs.add(new BasicNameValuePair("query_result_structure",
					queryResultStructure));
			request.setEntity(new UrlEncodedFormEntity(nvpairs, HTTP.UTF_8));
			HttpResponse response = httpclient.execute(request, localContext);
			HttpEntity entity = response.getEntity();
			EntityUtils.consume(entity);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void sendQueryResultData(int scenarioID, String queryResultData) {
		try {
			// login request
			String url = "http://" + HOST + "/upload_query_result_data/"
					+ scenarioID + "/";
			HttpPost request = new HttpPost(url);
			List<NameValuePair> nvpairs = new ArrayList<NameValuePair>();
			nvpairs.add(new BasicNameValuePair("query_result_data",
					queryResultData));
			request.setEntity(new UrlEncodedFormEntity(nvpairs, HTTP.UTF_8));
			HttpResponse response = httpclient.execute(request, localContext);
			HttpEntity entity = response.getEntity();
			EntityUtils.consume(entity);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void sendQueryResultCount(int scenarioID, String queryResultCount) {
		try {
			// login request
			String url = "http://" + HOST + "/upload_query_result_count/"
					+ scenarioID + "/";
			HttpPost request = new HttpPost(url);
			List<NameValuePair> nvpairs = new ArrayList<NameValuePair>();
			nvpairs.add(new BasicNameValuePair("query_result_count",
					queryResultCount));
			request.setEntity(new UrlEncodedFormEntity(nvpairs, HTTP.UTF_8));
			HttpResponse response = httpclient.execute(request, localContext);
			HttpEntity entity = response.getEntity();
			EntityUtils.consume(entity);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void shutdownClient() {
		// When HttpClient instance is no longer needed,
		// shut down the connection manager to ensure
		// immediate deallocation of all system resources
		httpclient.getConnectionManager().shutdown();
	}
}
