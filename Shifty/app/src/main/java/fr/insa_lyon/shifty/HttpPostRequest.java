package fr.insa_lyon.shifty;

import android.os.AsyncTask;
import android.os.StrictMode;
import android.util.Log;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;


/**
 * Created by Liuda on 04/05/2015.
 */

public class HttpPostRequest extends AsyncTask<String, String, String> {
    private List valeursPOST = new ArrayList();
    private SignInActivity signInActivity;
    private LogInActivity logInActivity;
    private int idActivity;

    @Override
    protected void onPreExecute() {
        // TODO Auto-generated method stub
        super.onPreExecute();
    }

    @Override
    protected void onPostExecute(String result) {
        // TODO Auto-generated method stub
        super.onPostExecute(result);
        System.out.println("Resultat de onPostExecute : -------------------" + result);
        switch (idActivity){
            case 1 :{
                try {
                    JSONObject res = new JSONObject(result);
                    if(res.getString("status").equals("error"))
                    {
                        CharSequence text = "Une erreur s'est produite lors de votre inscription!";
                        int duration = Toast.LENGTH_SHORT;
                        Toast toast = Toast.makeText(signInActivity.getApplicationContext(), text, duration);
                        toast.show();
                        break;
                    }else{
                        CharSequence text = "Inscription validée!";
                        int duration = Toast.LENGTH_SHORT;
                        Toast toast = Toast.makeText(signInActivity.getApplicationContext(), text, duration);
                        toast.show();
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }
                signInActivity.setPerson(result);
                break;
            }
            case 2 :{
                try {
                    JSONObject res = new JSONObject(result);
                    if(res.getString("status").equals("error"))
                    {
                        CharSequence text = "Login ou mot de passe incorrect!";
                        int duration = Toast.LENGTH_SHORT;
                        Toast toast = Toast.makeText(logInActivity.getApplicationContext(), text, duration);
                        toast.show();
                        break;
                    }else{
                        CharSequence text = "Login valide!";
                        int duration = Toast.LENGTH_SHORT;
                        Toast toast = Toast.makeText(logInActivity.getApplicationContext(), text, duration);
                        toast.show();
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }
                logInActivity.setPerson(result);
                break;
            }

        }
    }

    @Override
    protected String doInBackground(String... params) {
        StringBuilder response = new StringBuilder();
        try {
            HttpPost httppost = new HttpPost(params[0]);
            httppost.setEntity(new UrlEncodedFormEntity(valeursPOST));

            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse httpResponse = httpclient.execute(httppost);
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
            Log.e("[POST REQUEST]", e.getMessage());
        }

        return response.toString();
    }

    public void setValeursPOST(String id, String valeur){
        valeursPOST.add(new BasicNameValuePair(id, valeur));
    }

    public  void setSignInActivity(SignInActivity sga){
        signInActivity = sga;
        idActivity = 1;
    }

    public  void setLogInActivity(LogInActivity sga){
        logInActivity = sga;
        idActivity = 2;
    }
}

