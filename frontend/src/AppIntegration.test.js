import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import App from './App';

const mock = new MockAdapter(axios);

test('uploads 4 videos and receives optimization results', async () => {
  mock.onPost('http://localhost:5000/upload').reply(200, {
    north: 30,
    south: 25,
    west: 20,
    east: 15,
  });

  render(<App />);

  const input = screen.getByLabelText(/upload your traffic videos/i);
  fireEvent.change(input, {
    target: {
      files: [new File([], 'video1.mp4'), new File([], 'video2.mp4'), new File([], 'video3.mp4'), new File([], 'video4.mp4')],
    },
  });

  const button = screen.getByText(/run model/i);
  fireEvent.click(button);

  const northTime = await screen.findByText(/north: 30 seconds/i);
  expect(northTime).toBeInTheDocument();
});