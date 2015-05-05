package fr.insa_lyon.shifty;

import android.os.AsyncTask;
import android.os.StrictMode;
import android.util.Log;
import android.widget.EditText;
import android.widget.RadioGroup;

import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;


/**
 * Created by Liuda on 04/05/2015.
 */

public class HttpPostRequest extends AsyncTask<String, String, String> {
    private List valeursPOST = new ArrayList();

    @Override
    protected void onPreExecute() {
        // TODO Auto-generated method stub
        super.onPreExecute();
    }

    @Override
    protected String doInBackground(String... params) {

        try {
            HttpPost httppost = new HttpPost(params[0]);
            httppost.setEntity(new UrlEncodedFormEntity(valeursPOST));

            HttpClient httpclient = new DefaultHttpClient();
            httpclient.execute(httppost);

        } catch (Exception e) {
            Log.e("[POST REQUEST]", e.getMessage());
        }

        return null;
    }

    public void setValeursPOST(String id, String valeur){
        valeursPOST.add(new BasicNameValuePair(id,valeur));
    }
}

