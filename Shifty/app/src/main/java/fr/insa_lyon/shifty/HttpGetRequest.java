package fr.insa_lyon.shifty;

import android.os.AsyncTask;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Liuda on 04/05/2015.
 */
public class HttpGetRequest extends AsyncTask<String, String, String> {
    private List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
    HomeActivity home;

    @Override
    protected void onPreExecute() {
        // TODO Auto-generated method stub
        super.onPreExecute();
    }

    @Override
    protected void onPostExecute(String result) {
        // TODO Auto-generated method stub
        super.onPostExecute(result);
        System.out.println("Resultat de onPostExecute : -------------------"+result);
        home.setJson(result);

    }

    @Override
    protected String doInBackground(String... params) {
        StringBuilder response = new StringBuilder();
        try {

            String paramsString = URLEncodedUtils.format(nameValuePairs, "UTF-8");
            HttpGet get = new HttpGet(params[0] + "?" + paramsString);

            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpResponse httpResponse = httpClient.execute(get);
            if (httpResponse.getStatusLine().getStatusCode() == 200) {
                Log.d("[GET REQUEST]", "HTTP Get succeeded");
                HttpEntity messageEntity = httpResponse.getEntity();
                InputStream is = messageEntity.getContent();
                BufferedReader br = new BufferedReader(new InputStreamReader(is));
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
            }
        } catch (Exception e) {
            Log.e("[GET REQUEST]", e.getMessage());
        }
        System.out.println("-----------La reponse GET est : "+response.toString()+"------------");
        return response.toString();
    }

    public void setNameValuePairs(String id, String value){
        nameValuePairs.add(new BasicNameValuePair(id, value));
    }

    public void setActivityHome(HomeActivity ha){
        home = ha;
    }

}
