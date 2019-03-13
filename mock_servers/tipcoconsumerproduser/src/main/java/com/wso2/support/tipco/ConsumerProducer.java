package com.wso2.support.tipco;

import com.tibco.tibjms.Tibjms;
import com.tibco.tibjms.TibjmsTextMessage;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.ExceptionListener;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;
import java.util.Vector;

//Libraries needed to build SOAP message

public class ConsumerProducer implements ExceptionListener {

    private boolean useTopic = false;
    private int ackMode = Session.AUTO_ACKNOWLEDGE;
    private String corelation_id = null;

    private Session consumer_session = null;
    private Session producer_session = null;

    private MessageProducer msgProducer = null;

    private Vector<String> data = new Vector<String>();

    private ConsumerProducer() {
        try {

            String serverUrl = "tcp://localhost:7222";
            ConnectionFactory consumer_factory = new com.tibco.tibjms.TibjmsConnectionFactory(serverUrl);

            /* create the connection */
            String userName = "admin";
            String password = "";
            Connection consumer_connection = consumer_factory.createConnection(userName, password);

            /* create the session */
            consumer_session = consumer_connection.createSession(ackMode);

            /* set the exception listener */
            consumer_connection.setExceptionListener(this);

            /* start the connection */
            consumer_connection.start();

            ConnectionFactory producer_factory = new com.tibco.tibjms.TibjmsConnectionFactory(serverUrl);

            Connection producer_connection = producer_factory.createConnection(userName, password);

            /* create the session */
            producer_session = producer_connection.createSession(javax.jms.Session.AUTO_ACKNOWLEDGE);

            producer_connection.start();

            Consume();
        } catch (JMSException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {

        new ConsumerProducer();
    }

    private void Consume() throws JMSException {
        Message msg = null;
        String msgType = "UNKNOWN";

        String consumer_queue_name = "Request";
        System.err.println("Subscribing to destination: " + consumer_queue_name + "\n");


        /* create the destination */
        Destination consumer_destination = null;
        if (useTopic)
            consumer_destination = consumer_session.createTopic(consumer_queue_name);
        else
            consumer_destination = consumer_session.createQueue(consumer_queue_name);

        /* create the consumer */
        MessageConsumer msgConsumer = consumer_session.createConsumer(consumer_destination);



        /* read messages */
        while (true) {
            /* receive the message */
            msg = msgConsumer.receive();
            //corelation_id = msg.getJMSCorrelationID();
            corelation_id = msg.getJMSMessageID();
            //corelation_id=msg.getJMSCorrelationID();
            System.err.println(System.currentTimeMillis() + "++++++++++++++++++++" + corelation_id
                    + "++++++++++++++++++++++++++++++++" + "message recieved");
            if (ackMode == Session.CLIENT_ACKNOWLEDGE || ackMode == Tibjms.EXPLICIT_CLIENT_ACKNOWLEDGE
                    || ackMode == Tibjms.EXPLICIT_CLIENT_DUPS_OK_ACKNOWLEDGE) {
                msg.acknowledge();
            }
          /* try {
                TimeUnit.SECONDS.sleep(60);
            }catch (Exception e){
                System.err.println(e.toString());
            }*/

            data.clear();
            data.add(msg.toString());
            System.err.println("is get delivery ++++++++++++++++++" + msg.getJMSRedelivered());
            if (((TibjmsTextMessage) msg).getText().equals("<outonly/>") && msg.getJMSReplyTo() != null) {
                System.out.println("!!!Suspicious message, found reply to (getJMSReplyTo) in out only message !!! ");
                continue;
            }
            publish(msg.getJMSReplyTo());

        }

    }

    private void publish(Destination replyDest) {
        if (replyDest != null) {

            System.err.println("reply destination++++++++++++++++++++++++++++" + replyDest.toString());

            try {
                TextMessage msg;
                int i;

                if (data.size() == 0) {
                    System.err.println("***Error: must specify at least one message text\n");
                }

                System.err.println("Publishing to destination '" + replyDest);

                /* create the destination */
                Destination producer_destination = null;
                String producer_queue_name = "Response";
                if (useTopic)
                    producer_destination = producer_session.createTopic(producer_queue_name);
                else {
                    //  producer_destination = producer_session.createQueue(replyDest.toString());
                    /* create the producer */
                    msgProducer = producer_session.createProducer(replyDest);

                }

                /* publish messages */
                for (i = 0; i < data.size(); i++) {
                    /* create text message */
                    msg = producer_session.createTextMessage();
                    msg.setJMSCorrelationID(corelation_id);

                    /* set message text */
                    //                msg.setText(data.elementAt(i));
                    //                    msg.setText("{\"hello\": \"world\"}");
                    //                    msg.setStringProperty("Content-Type", "application/json");

                    msg.setText("<div>Hello World</div>");
                    msg.setStringProperty("Content-Type", "application/xml");

                    /* publish message */

                    try {
                        Thread.sleep(300);
                    } catch (Exception e) {
                        System.err.println(e);
                    }
                    msgProducer.send(msg);

                    System.err.println(System.currentTimeMillis() + "+++++++++++++++++++++++++++++++" + corelation_id
                            + "++++++++++++++++++++++++++++++++++++ message published \n");
                }

                msgProducer.close();

                /* close the connection */
                //            producer_connection.close();
            } catch (JMSException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        } else {
            System.out.println("Reply to Dest null");
        }
    }

    public void onException(JMSException e) {
        /* print the connection exception status */
        System.err.println("CONNECTION EXCEPTION: " + e.getMessage());
    }

}
