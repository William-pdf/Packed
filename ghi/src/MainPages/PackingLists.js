import React, { useState, useEffect, useContext } from "react";
import AuthContext from "../context/AuthContext";
import { loadPackingLists } from "./MainApi";
import { Card, Row, Col, Container } from "react-bootstrap";
import "./pages.css";

export const PackingLists = () => {
  const [packingLists, setPackingLists] = useState([]);
  const { authTokens } = useContext(AuthContext);

  const imageClasses = ["img_01", "img_02", "img_03", "img_04", "img_05"];

  useEffect(() => {
    async function fetchData() {
      const packingLists = await loadPackingLists(authTokens);
      setPackingLists(packingLists);
    }
    fetchData();
  }, [authTokens]);

  return (
    <Container className="main-container shadow">
      <Row>
        {packingLists.map((list, k) => (
          <Col key={k} xs={12} md={6} lg={4}>
            <Card className={imageClasses[list.id % 5]}>
              <Card.Body>
                <div className="card-details">
                  <Card.Title>{list.title}</Card.Title>
                  <Card.Subtitle>created: {list.created}</Card.Subtitle>
                  <Card.Text>
                    Departure: {list.departure_date}
                    <br />
                    Return: {list.return_date}
                  </Card.Text>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};